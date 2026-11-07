import json
import os
import tempfile
import unittest
import uuid
from datetime import datetime

SAMPLE_DIR = "sample_data"
ORDERS_FILE = os.path.join(SAMPLE_DIR, "orders.json")
CATALOG_FILE = os.path.join(SAMPLE_DIR, "catalog.json")


class OrderError(Exception):
    pass


class Product:
    def __init__(self, pid, name, price, stock):
        if not isinstance(pid, str) or not pid.strip():
            raise ValueError("product id cannot be empty")
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            raise ValueError(f"bad price for product {pid}")
        if isinstance(stock, bool) or not isinstance(stock, int) or stock < 0:
            raise ValueError(f"bad stock for product {pid}")
        self.product_id = pid.strip()
        self.name = name
        self.price = price
        self.stock = stock


class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self, product):
        if product.product_id in self._products:
            raise ValueError(f"duplicate product id: {product.product_id}")
        self._products[product.product_id] = product

    def load_catalog(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                items = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise OrderError(f"Could not read catalog '{path}': {e}")

        if not isinstance(items, list):
            raise OrderError("Catalog must be a list of products")
        for item in items:
            try:
                self.add_product(Product(item["id"], item["name"], item["price"], item["stock"]))
            except (KeyError, TypeError, ValueError) as e:
                raise OrderError(f"Bad catalog entry {item}: {e}")

    def get_product(self, pid):
        if pid not in self._products:
            raise OrderError(f"Unknown product: {pid}")
        return self._products[pid]

    def stock_snapshot(self):
        return {pid: p.stock for pid, p in self._products.items()}

    def restore_stock(self, snap):
        for pid, stock in snap.items():
            self._products[pid].stock = stock

    def reduce_stock(self, items):
        for pid, qty in items.items():
            self._products[pid].stock -= qty


class Cart:
    def __init__(self, inventory):
        self._inventory = inventory
        self.items = {}
        self.discount_percent = 0

    def add_item(self, pid, qty):
        if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
            raise OrderError("Quantity must be a whole number greater than zero")
        self._inventory.get_product(pid)
        self.items[pid] = self.items.get(pid, 0) + qty

    def set_discount(self, pct):
        if isinstance(pct, bool) or not isinstance(pct, (int, float)):
            raise OrderError("Discount must be a number")
        if not 0 <= pct <= 100:
            raise OrderError("Discount must be 0-100")
        self.discount_percent = pct

    def subtotal(self):
        return sum(self._inventory.get_product(pid).price * q
                   for pid, q in self.items.items())

    def total(self):
        return round(self.subtotal() * (1 - self.discount_percent / 100), 2)

    def clear(self):
        self.items = {}


class Order:
    def __init__(self, order_id, lines, discount, subtotal, total):
        self.order_id = order_id
        self.lines = lines
        self.discount_percent = discount
        self.subtotal = subtotal
        self.total = total
        self.created_at = datetime.now().isoformat(timespec="seconds")

    def to_dict(self):
        return {"order_id": self.order_id, "created_at": self.created_at,
                "items": self.lines, "discount_percent": self.discount_percent,
                "subtotal": self.subtotal, "total": self.total}


def load_orders(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            orders = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise OrderError(f"Could not read orders: {e}")
    if not isinstance(orders, list):
        raise OrderError("Orders file has wrong format")
    return orders


def save_orders(path, orders):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=2)
    os.replace(tmp, path)


def place_order(cart, inventory, orders_path):
    if not cart.items:
        raise OrderError("Cart is empty")

    for pid, qty in cart.items.items():
        p = inventory.get_product(pid)
        if qty > p.stock:
            raise OrderError(f"Not enough stock for {p.name}: wanted {qty}, have {p.stock}")

    old_orders = load_orders(orders_path)
    used = {o["order_id"] for o in old_orders}

    oid = "ORD-" + uuid.uuid4().hex[:8].upper()
    while oid in used:
        oid = "ORD-" + uuid.uuid4().hex[:8].upper()

    lines = []
    for pid, qty in cart.items.items():
        p = inventory.get_product(pid)
        lines.append({"product_id": pid, "name": p.name,
                      "quantity": qty, "unit_price": p.price})
    order = Order(oid, lines, cart.discount_percent, cart.subtotal(), cart.total())

    snap = inventory.stock_snapshot()
    inventory.reduce_stock(cart.items)
    try:
        save_orders(orders_path, old_orders + [order.to_dict()])
    except (OSError, TypeError, ValueError) as e:
        inventory.restore_stock(snap)
        raise OrderError(f"Could not save order, stock restored: {e}")

    cart.clear()
    return order


class TestOrderSystem(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.folder = temp.name
        self.catalog_path = os.path.join(self.folder, "catalog.json")
        self.orders_path = os.path.join(self.folder, "orders.json")

        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump([{"id": "P1", "name": "Pen", "price": 100, "stock": 5},
                       {"id": "P2", "name": "Book", "price": 50, "stock": 1}], f)

        self.inventory = Inventory()
        self.inventory.load_catalog(self.catalog_path)

    def test_total_and_stock(self):
        cart = Cart(self.inventory)
        cart.add_item("P1", 2)
        cart.set_discount(10)
        order = place_order(cart, self.inventory, self.orders_path)
        self.assertEqual(order.total, 180)
        self.assertEqual(self.inventory.get_product("P1").stock, 3)
        self.assertEqual(len(load_orders(self.orders_path)), 1)

    def test_out_of_stock(self):
        cart = Cart(self.inventory)
        cart.add_item("P1", 2)
        cart.add_item("P2", 5)
        with self.assertRaises(OrderError):
            place_order(cart, self.inventory, self.orders_path)
        self.assertEqual(self.inventory.get_product("P1").stock, 5)
        self.assertEqual(self.inventory.get_product("P2").stock, 1)

    def test_bad_quantity(self):
        cart = Cart(self.inventory)
        for q in (0, -3, 2.5, "2"):
            with self.assertRaises(OrderError):
                cart.add_item("P1", q)

    def test_stock_restored_on_save_fail(self):
        bad = os.path.join(self.folder, "missing_folder", "orders.json")
        cart = Cart(self.inventory)
        cart.add_item("P1", 2)
        with self.assertRaises(OrderError):
            place_order(cart, self.inventory, bad)
        self.assertEqual(self.inventory.get_product("P1").stock, 5)

    def test_unique_ids(self):
        ids = set()
        for _ in range(3):
            cart = Cart(self.inventory)
            cart.add_item("P1", 1)
            ids.add(place_order(cart, self.inventory, self.orders_path).order_id)
        self.assertEqual(len(ids), 3)
        self.assertEqual(len(load_orders(self.orders_path)), 3)


def main():
    os.makedirs(SAMPLE_DIR, exist_ok=True)

    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump([{"id": "P1", "name": "Pen", "price": 100, "stock": 5},
                   {"id": "P2", "name": "Notebook", "price": 250, "stock": 2}], f, indent=2)
    if os.path.exists(ORDERS_FILE):
        os.remove(ORDERS_FILE)

    inventory = Inventory()
    inventory.load_catalog(CATALOG_FILE)

    cart = Cart(inventory)
    cart.add_item("P1", 2)
    cart.set_discount(10)
    print("Cart total:", cart.total())
    order = place_order(cart, inventory, ORDERS_FILE)
    print("Order placed:", order.order_id, "| total:", order.total)
    print("Stock of P1 is now:", inventory.get_product("P1").stock)

    cart.add_item("P2", 10)
    try:
        place_order(cart, inventory, ORDERS_FILE)
    except OrderError as e:
        print("Error:", e)

    print("\nRunning unit tests...")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestOrderSystem)
    unittest.TextTestRunner(verbosity=1).run(suite)


if __name__ == "__main__":
    main()