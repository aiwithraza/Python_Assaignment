import csv
import os

SAMPLE_DIR = "sample_data"


def check_columns(found_columns, needed_columns, file_path):
    if found_columns is None:
        raise ValueError(f"{file_path} is empty")
    missing = [name for name in needed_columns if name not in found_columns]
    if missing:
        raise ValueError(f"{file_path} is missing columns: {missing}")


def read_inventory(path):
    inventory = {}
    with open(path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        check_columns(reader.fieldnames, ["sku", "name", "quantity"], path)

        for row in reader:
            sku = (row.get("sku") or "").strip()
            name = (row.get("name") or "").strip()
            if not sku:
                raise ValueError("Inventory has a row without a SKU")
            if sku in inventory:
                raise ValueError(f"Duplicate SKU in inventory: {sku}")
            try:
                quantity = int((row.get("quantity") or "").strip())
            except ValueError:
                raise ValueError(f"Quantity of {sku} is not a whole number")
            if quantity < 0:
                raise ValueError(f"Quantity of {sku} is negative")
            inventory[sku] = {"name": name, "quantity": quantity}
    return inventory


def apply_movements(inventory, movements_path):
    rejected = []

    with open(movements_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        check_columns(reader.fieldnames, ["sku", "type", "units"], movements_path)

        for row in reader:
            sku = (row.get("sku") or "").strip()
            raw_type = (row.get("type") or "").strip()
            raw_units = (row.get("units") or "").strip()
            kind = raw_type.upper()
            reason = None

            if sku not in inventory:
                reason = "Unknown SKU"
            elif kind not in ("IN", "OUT"):
                reason = "Invalid movement type"
            else:
                try:
                    units = int(raw_units)
                except ValueError:
                    reason = "Units is not a whole number"
                else:
                    if units <= 0:
                        reason = "Units must be greater than zero"
                    elif kind == "OUT" and units > inventory[sku]["quantity"]:
                        reason = "Not enough stock"

            if reason:
                rejected.append({"sku": sku, "type": raw_type, "units": raw_units, "reason": reason})
                continue

            if kind == "IN":
                inventory[sku]["quantity"] += units
            else:
                inventory[sku]["quantity"] -= units

    return rejected


def write_inventory(path, inventory):
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["sku", "name", "quantity"])
        for sku, item in inventory.items():
            writer.writerow([sku, item["name"], item["quantity"]])


def write_rejected(path, rejected):
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["sku", "type", "units", "reason"])
        writer.writeheader()
        writer.writerows(rejected)


def create_sample_inventory_files(inventory_path, movements_path):
    with open(inventory_path, "w", newline="", encoding="utf-8") as f:
        f.write("sku,name,quantity\nP01,Pen,10\nP02,Notebook,5\nP03,Marker,0\n")
    with open(movements_path, "w", newline="", encoding="utf-8") as f:
        f.write("sku,type,units\n"
                "P01,OUT,4\n"
                "P01,OUT,9\n"
                "P01,IN,2\n"
                "P99,IN,5\n"
                "P02,IN,0\n"
                "P02,MOVE,3\n"
                "P02,OUT,-1\n"
                "P02,OUT,abc\n"
                "P03,IN,7\n")


def main():
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    inventory_path = os.path.join(SAMPLE_DIR, "inventory.csv")
    movements_path = os.path.join(SAMPLE_DIR, "movements.csv")
    updated_path = os.path.join(SAMPLE_DIR, "updated_inventory.csv")
    rejected_path = os.path.join(SAMPLE_DIR, "rejected_movements.csv")

    create_sample_inventory_files(inventory_path, movements_path)

    inventory = read_inventory(inventory_path)
    rejected = apply_movements(inventory, movements_path)
    write_inventory(updated_path, inventory)
    write_rejected(rejected_path, rejected)

    print("Updated stock:")
    for sku, item in inventory.items():
        print(f"  {sku} {item['name']:<10} {item['quantity']}")
    print("Rejected movements:")
    for row in rejected:
        print("  ", row)
    print("Files written: updated_inventory.csv, rejected_movements.csv")


if __name__ == "__main__":
    main()