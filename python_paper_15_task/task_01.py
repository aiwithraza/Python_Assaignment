REQUIRED_KEYS = ["id", "customer", "category", "amount", "status"]


def check_transactions(transactions):
    seen_ids = set()

    for t in transactions:
        for key in REQUIRED_KEYS:
            if key not in t:
                raise ValueError(f"Transaction is missing '{key}': {t}")

        if t["id"] in seen_ids:
            raise ValueError(f"Duplicate transaction id: {t['id']}")
        seen_ids.add(t["id"])

        amount = t["amount"]
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise ValueError(f"Amount must be a number (id {t['id']})")
        if amount < 0:
            raise ValueError(f"Amount cannot be negative (id {t['id']})")


def get_top_category(category_totals):
    if not category_totals:
        return None
    best = sorted(category_totals.items(), key=lambda item: (-item[1], item[0]))
    return best[0][0]


def analyze_transactions(transactions):
    check_transactions(transactions)

    totals = {}
    categories = {}

    for t in transactions:
        name = t["customer"]

        if name not in totals:
            totals[name] = 0
            categories[name] = {}

        if t["status"].lower() != "success":
            continue

        totals[name] += t["amount"]
        cat = t["category"]
        categories[name][cat] = categories[name].get(cat, 0) + t["amount"]

    report = [
        {
            "customer": name,
            "total": totals[name],
            "top_category": get_top_category(categories[name]),
        }
        for name in totals
    ]

    report.sort(key=lambda row: (-row["total"], row["customer"]))

    rank = 0
    previous_total = None
    for position, row in enumerate(report, start=1):
        if row["total"] != previous_total:
            rank = position
            previous_total = row["total"]
        row["rank"] = rank

    return report


def main():
    sample = [
        {"id": 1, "customer": "Ali", "category": "Food", "amount": 500, "status": "success"},
        {"id": 2, "customer": "Ali", "category": "Travel", "amount": 200, "status": "failed"},
        {"id": 3, "customer": "Sara", "category": "Food", "amount": 700, "status": "success"},
        {"id": 4, "customer": "Zain", "category": "Shopping", "amount": 300, "status": "failed"},
    ]

    print(f"{'Rank':<6}{'Customer':<12}{'Total':<10}Top Category")
    for row in analyze_transactions(sample):
        print(f"{row['rank']:<6}{row['customer']:<12}{row['total']:<10}{row['top_category']}")

    try:
        analyze_transactions(sample + [sample[0]])
    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()