# Encode/decode speed: the same order as JSON (stdlib `json`) and as Protobuf (the `protobuf` library).
# Use when: you want real numbers for your own message on your own machine, not a claim.
# Docs: https://protobuf.dev/overview/ and https://github.com/protocolbuffers/protobuf/blob/main/python/README.md
# Needs `pip install protobuf`. The schema is built in code here, so no `protoc` step is needed.
# Times are true only for this machine, this Python and this protobuf backend.
import json
import sys
import time

try:
    from google.protobuf import descriptor_pb2, descriptor_pool, message_factory
    from google.protobuf.internal import api_implementation
except ImportError:
    print("Install the protobuf library first: pip install protobuf")
    sys.exit(0)

ORDER = {"id": 42, "customer": "Ali",
         "items": [{"name": "Biryani", "qty": 2, "price_cents": 450},
                   {"name": "Lassi", "qty": 1, "price_cents": 150}],
         "total_cents": 1050}
N = 100_000


def build_order_class():
    # message Item  { string name = 1; int32 qty = 2; int32 price_cents = 3; }
    # message Order { int32 id = 1; string customer = 2; repeated Item items = 3; int32 total_cents = 4; }
    F = descriptor_pb2.FieldDescriptorProto
    file = descriptor_pb2.FileDescriptorProto(name="order.proto", package="shop", syntax="proto3")
    item = file.message_type.add(name="Item")
    item.field.add(name="name", number=1, type=F.TYPE_STRING, label=F.LABEL_OPTIONAL)
    item.field.add(name="qty", number=2, type=F.TYPE_INT32, label=F.LABEL_OPTIONAL)
    item.field.add(name="price_cents", number=3, type=F.TYPE_INT32, label=F.LABEL_OPTIONAL)
    order = file.message_type.add(name="Order")
    order.field.add(name="id", number=1, type=F.TYPE_INT32, label=F.LABEL_OPTIONAL)
    order.field.add(name="customer", number=2, type=F.TYPE_STRING, label=F.LABEL_OPTIONAL)
    order.field.add(name="items", number=3, type=F.TYPE_MESSAGE, label=F.LABEL_REPEATED, type_name=".shop.Item")
    order.field.add(name="total_cents", number=4, type=F.TYPE_INT32, label=F.LABEL_OPTIONAL)
    pool = descriptor_pool.DescriptorPool()
    pool.AddSerializedFile(file.SerializeToString())
    desc =pool.FindMessageTypeByName("shop.Order")
    if hasattr(message_factory, "GetMessageClass"):  # protobuf 4.x and later
        return message_factory.GetMessageClass(desc)
    return message_factory.MessageFactory(pool).GetPrototype(desc)  # protobuf 3.x


def per_op_us(fn) -> float:
    start = time.perf_counter()
    for _ in range(N):
        fn()
    return (time.perf_counter() - start) / N * 1e6  # microseconds per call


Order = build_order_class()
msg = Order(**ORDER)
json_bytes = json.dumps(ORDER, separators=(",", ":")).encode()
proto_bytes = msg.SerializeToString()

print(f"protobuf backend: {api_implementation.Type()}, {N:,} runs each")
print(f"JSON encode:     {per_op_us(lambda: json.dumps(ORDER, separators=(',', ':')).encode()):.2f} µs")
print(f"JSON decode:     {per_op_us(lambda: json.loads(json_bytes)):.2f} µs")
print(f"Protobuf encode: {per_op_us(msg.SerializeToString):.2f} µs")
print(f"Protobuf decode: {per_op_us(lambda: Order.FromString(proto_bytes)):.2f} µs")

# Both round-trip to the same order; the sizes match request_payload_size.py.
assert json.loads(json_bytes) == ORDER
assert Order.FromString(proto_bytes) == msg and msg.items[1].name == "Lassi"
assert len(json_bytes) == 143 and len(proto_bytes) == 40
