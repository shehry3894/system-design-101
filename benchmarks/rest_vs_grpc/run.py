# REST (FastAPI + JSON) vs gRPC (grpcio + Protobuf) for the same "get order" call, on one machine.
# Scenarios follow grpc.io's benchmarking guide: contentionless latency (one call at a time)
# and throughput (many calls in flight, from several client processes so the client is not the limit).
# Run: python run.py            (full run, about two minutes)
#      python run.py --quick    (smoke test, about 20 seconds)
import asyncio
import json
import os
import socket
import statistics
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from pathlib import Path

os.environ.setdefault("GRPC_VERBOSITY", "ERROR")  # hide grpc's fork() info lines from `ps` calls
HERE = Path(__file__).parent
if not (HERE / "order_pb2_grpc.py").exists():  # generate the Protobuf and gRPC code from order.proto
    subprocess.run([sys.executable, "-m", "grpc_tools.protoc", "-I.", "--python_out=.",
                    "--grpc_python_out=.", "order.proto"], cwd=HERE, check=True)
sys.path.insert(0, str(HERE))

import aiohttp  # noqa: E402
import grpc  # noqa: E402
import httpx  # noqa: E402
from google.protobuf.internal import api_implementation  # noqa: E402
from google.protobuf.json_format import MessageToDict  # noqa: E402

import order_pb2  # noqa: E402
import order_pb2_grpc  # noqa: E402
from order_data import make_order  # noqa: E402

QUICK = "--quick" in sys.argv
SIZES = {"small (2 items)": 2, "medium (100 items)": 100, "large (1,000 items)": 1000}
STYLES = ["REST, aiohttp client", "REST, httpx client", "gRPC"]
LATENCY_CALLS = 300 if QUICK else 5000
WARMUP_CALLS = 50 if QUICK else 500
THROUGHPUT_SECONDS = 1 if QUICK else 5
CLIENT_PROCESSES, IN_FLIGHT_EACH = 4, 16  # 64 calls in flight in total
REST_PORT, GRPC_PORT = 8011, 50061


# ---- clients: each returns (call(n) -> decoded order, close()) ----

async def open_client(style: str, rest_port: int = REST_PORT, grpc_port: int = GRPC_PORT):
    if style == "gRPC":
        channel = grpc.aio.insecure_channel(f"127.0.0.1:{grpc_port}")  # one channel, reused (grpc.io advice)
        stub = order_pb2_grpc.OrdersStub(channel)

        async def call(n):
            return await stub.GetOrder(order_pb2.GetOrderRequest(id=42, item_count=n))
        return call, channel.close
    base = f"http://127.0.0.1:{rest_port}/orders/42?items="
    if style == "REST, aiohttp client":
        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=IN_FLIGHT_EACH))

        async def call(n):
            async with session.get(base + str(n)) as r:
                r.raise_for_status()
                return await r.json()
        return call, session.close
    client = httpx.AsyncClient(limits=httpx.Limits(max_connections=IN_FLIGHT_EACH))

    async def call(n):
        r = await client.get(base + str(n))
        r.raise_for_status()
        return r.json()
    return call, client.aclose


# ---- measurements ----

async def latency(style: str, n: int) -> dict:
    call, close = await open_client(style)
    for _ in range(WARMUP_CALLS):
        await call(n)
    times = []
    for _ in range(LATENCY_CALLS):
        start = time.perf_counter()
        await call(n)
        times.append((time.perf_counter() - start) * 1e6)
    await close()
    times.sort()
    return {"p50": times[len(times) // 2], "p99": times[int(len(times) * 0.99)], "mean": statistics.fmean(times)}


async def _client_load(style: str, n: int, stop_at: float) -> tuple[int, float]:
    call, close = await open_client(style)
    for _ in range(IN_FLIGHT_EACH):  # open the connections before the clock starts
        await call(n)
    done = 0

    async def worker():
        nonlocal done
        while time.time() < stop_at:
            await call(n)
            done += 1

    cpu0 = time.process_time()
    await asyncio.gather(*(worker() for _ in range(IN_FLIGHT_EACH)))
    cpu = time.process_time() - cpu0
    await close()
    return done, cpu


def client_process(style: str, n: int, start_at: float, stop_at: float) -> tuple[int, float]:
    time.sleep(max(0.0, start_at - time.time()))  # all client processes start together
    return asyncio.run(_client_load(style, n, stop_at))


def throughput(pool, style: str, n: int, server_pid: int) -> dict:
    start_at = time.time() + 1.5  # time for the client processes to connect
    stop_at = start_at + THROUGHPUT_SECONDS
    cpu0 = None
    futures = [pool.submit(client_process, style, n, start_at, stop_at) for _ in range(CLIENT_PROCESSES)]
    time.sleep(max(0.0, start_at - time.time()))
    cpu0 = cpu_seconds(server_pid)
    results = [f.result() for f in futures]
    server_cpu = cpu_seconds(server_pid) - cpu0
    calls = sum(r[0] for r in results)
    return {"qps": calls / THROUGHPUT_SECONDS, "server_cpu_us": server_cpu / calls * 1e6,
            "client_cpu_us": sum(r[1] for r in results) / calls * 1e6}


def cpu_seconds(pid: int) -> float:
    """Total CPU time (user + system) of a process and its threads, from `ps`."""
    out = subprocess.run(["ps", "-o", "time=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    secs = 0.0
    for part in out.replace("-", ":").split(":"):
        secs = secs * 60 + float(part)
    return secs


# ---- bytes on the wire: a TCP proxy that counts what passes through it ----

async def wire_bytes(style: str, n: int, calls: int = 200) -> tuple[float, float]:
    counts = {"up": 0, "down": 0}

    async def handle(reader, writer):
        target = GRPC_PORT if style == "gRPC" else REST_PORT
        t_reader, t_writer = await asyncio.open_connection("127.0.0.1", target)

        async def pipe(src, dst, key):
            while data := await src.read(65536):
                counts[key] += len(data)
                dst.write(data)
                await dst.drain()
            dst.close()

        await asyncio.gather(pipe(reader, t_writer, "up"), pipe(t_reader, writer, "down"))

    proxy = await asyncio.start_server(handle, "127.0.0.1", 0)
    port = proxy.sockets[0].getsockname()[1]
    call, close = await open_client(style, rest_port=port, grpc_port=port)
    for _ in range(10):  # connection setup and first headers are not counted
        await call(n)
    counts["up"] = counts["down"] = 0
    for _ in range(calls):
        await call(n)
    await close()
    proxy.close()
    return counts["up"] / calls, counts["down"] / calls


# ---- driver ----

def wait_for_port(port: int, timeout: float = 20):
    end = time.time() + timeout
    while time.time() < end:
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) == 0:
                return
        time.sleep(0.1)
    raise RuntimeError(f"server on port {port} did not start")


async def check_same_answer():
    for style in STYLES:
        call, close = await open_client(style)
        for n in SIZES.values():
            got = await call(n)
            if style == "gRPC":
                got = MessageToDict(got, preserving_proto_field_name=True)
                got["id"], got["total_cents"] = int(got["id"]), int(got["total_cents"])
            assert got == make_order(42, n), f"{style} returned a different order"
        await close()


def bench(server_pids: dict) -> dict:
    asyncio.run(check_same_answer())
    results = {}
    with ProcessPoolExecutor(CLIENT_PROCESSES, mp_context=get_context("spawn")) as pool:
        for label, n in SIZES.items():
            order = make_order(42, n)
            body = {"REST": len(json.dumps(order, separators=(",", ":")).encode()),
                    "gRPC": order_pb2.Order(**order).ByteSize()}
            for style in STYLES:
                row = asyncio.run(latency(style, n))
                row.update(throughput(pool, style, n, server_pids[style]))
                row["wire"] = asyncio.run(wire_bytes(style, n))
                row["body"] = body["gRPC" if style == "gRPC" else "REST"]
                results[(label, style)] = row
    return results


def report(results: dict):
    print(f"protobuf backend: {api_implementation.Type()}; latency: {LATENCY_CALLS:,} calls, one at a time; "
          f"throughput: {CLIENT_PROCESSES} client processes x {IN_FLIGHT_EACH} in flight for {THROUGHPUT_SECONDS} s\n")
    print("| Message | Style | Body bytes | Wire bytes per call (up / down) | p50 µs | p99 µs "
          "| Calls/s | Server CPU µs per call | Client CPU µs per call |")
    print("|---|---|---|---|---|---|---|---|---|")
    for (label, style), r in results.items():
        up, down = r["wire"]
        print(f"| {label} | {style} | {r['body']:,} | {up:,.0f} / {down:,.0f} | {r['p50']:,.0f} | {r['p99']:,.0f} "
              f"| {r['qps']:,.0f} | {r['server_cpu_us']:,.0f} | {r['client_cpu_us']:,.0f} |")


def main():
    assert api_implementation.Type() == "upb", "use protobuf's default upb backend"
    rest = subprocess.Popen([sys.executable, "-m", "uvicorn", "rest_server:app", "--port", str(REST_PORT),
                             "--log-level", "warning", "--no-access-log"], cwd=HERE)
    grpc_server = subprocess.Popen([sys.executable, "grpc_server.py", str(GRPC_PORT)], cwd=HERE)
    try:
        wait_for_port(REST_PORT)
        wait_for_port(GRPC_PORT)
        pids = {"REST, aiohttp client": rest.pid, "REST, httpx client": rest.pid, "gRPC": grpc_server.pid}
        report(bench(pids))
    finally:
        for p in (rest, grpc_server):
            p.terminate()
            p.wait()


if __name__ == "__main__":
    main()
