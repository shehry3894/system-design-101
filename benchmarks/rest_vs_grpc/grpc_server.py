# gRPC: grpcio asyncio server, Protobuf over HTTP/2. Run by run.py: python grpc_server.py <port>
import asyncio
import sys

import grpc

import order_pb2
import order_pb2_grpc
from order_data import make_order


class Orders(order_pb2_grpc.OrdersServicer):
    def __init__(self):
        self.cache = {}  # built once, so calls measure serving, not building

    async def GetOrder(self, request, context):
        key = (request.id, request.item_count)
        if key not in self.cache:
            self.cache[key] = order_pb2.Order(**make_order(*key))
        return self.cache[key]


async def main(port: int):
    server = grpc.aio.server()
    order_pb2_grpc.add_OrdersServicer_to_server(Orders(), server)
    server.add_insecure_port(f"127.0.0.1:{port}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1])))
