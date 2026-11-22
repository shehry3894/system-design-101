# Payload size: the same order as JSON and as Protobuf (Protocol Buffers).
# Use when: choosing an API style and the bytes on the wire matter (mobile, high volume).
# Docs: https://protobuf.dev/programming-guides/encoding/
# Real projects use the `protobuf` library and a .proto file. Here the bytes are written
# by hand, so you can see why they are fewer: field numbers instead of names, varints.
import json

ORDER = {"id": 42, "customer": "Ali",
         "items": [{"name": "Biryani", "qty": 2, "price_cents": 450},
                   {"name": "Lassi", "qty": 1, "price_cents": 150}],
         "total_cents": 1050}
# message Item  { string name = 1; int32 qty = 2; int32 price_cents = 3; }
# message Order { int32 id = 1; string customer = 2; repeated Item items = 3; int32 total_cents = 4; }


def varint(n: int) -> bytes:
    n &= (1 << 64) - 1  # negatives: 64-bit two's complement, so always 10 bytes
    out = bytearray()
    while True:
        low, n = n & 0x7F, n >> 7
        out.append(low | (0x80 if n else 0))  # top bit set = more bytes follow
        if not n:
            return bytes(out)


def field_int(number: int, value: int) -> bytes:
    return varint(number << 3 | 0) + varint(value)  # tag (wire type 0) + value


def field_bytes(number: int, data: bytes) -> bytes:
    return varint(number << 3 | 2) + varint(len(data)) + data  # tag (wire type 2) + length + data


def encode_order(order: dict) -> bytes:
    def item(i):
        return field_bytes(1, i["name"].encode()) + field_int(2, i["qty"]) + field_int(3, i["price_cents"])
    return (field_int(1, order["id"]) + field_bytes(2, order["customer"].encode())
            + b"".join(field_bytes(3, item(i)) for i in order["items"])
            + field_int(4, order["total_cents"]))


json_bytes = json.dumps(ORDER, separators=(",", ":")).encode()
proto_bytes = encode_order(ORDER)
print(f"JSON: {len(json_bytes)} bytes")
print(f"Protobuf: {len(proto_bytes)} bytes")

# The examples on protobuf.dev "Encoding", byte for byte
assert field_int(1, 150) == bytes.fromhex("089601")
assert field_bytes(2, b"testing") == bytes.fromhex("120774657374696e67")
assert field_bytes(3, field_int(1, 150)) == bytes.fromhex("1a03089601")
assert len(field_int(1, -2)) == 11                                 # negative int32: 10-byte varint
assert len(json.dumps({"a": -2}, separators=(",", ":"))) == 8
assert len(json_bytes) == 143 and len(proto_bytes) == 40
