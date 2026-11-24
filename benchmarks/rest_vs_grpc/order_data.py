# The same order for both servers. With 2 items it is the order in examples/communication/.
MENU = [("Biryani", 2, 450), ("Lassi", 1, 150)]


def make_order(order_id: int, item_count: int) -> dict:
    items = [{"name": n, "qty": q, "price_cents": p} for n, q, p in (MENU[i % 2] for i in range(item_count))]
    return {"id": order_id, "customer": "Ali", "items": items,
            "total_cents": sum(i["qty"] * i["price_cents"] for i in items)}
