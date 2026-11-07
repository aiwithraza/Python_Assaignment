import json
import os

CONTACTS_FILE = os.path.join("sample_data", "contacts.json")


class StorageError(Exception):
    pass


def load_contacts(path):
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        raise StorageError(f"'{path}' is corrupt (bad JSON). File was not modified.")
    except OSError as e:
        raise StorageError(f"Could not read '{path}': {e}")

    if not isinstance(data, list):
        raise StorageError(f"'{path}' has wrong format (expected list)")

    ids = set()
    for c in data:
        ok = (isinstance(c, dict)
              and isinstance(c.get("id"), int)
              and all(isinstance(c.get(k), str) for k in ("name", "phone", "email")))
        if not ok or c["id"] in ids:
            raise StorageError(f"'{path}' has a bad or duplicate entry: {c}")
        ids.add(c["id"])
    return data


def save_contacts(path, contacts):
    tmp = path + ".tmp"
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(contacts, f, indent=2)
        os.replace(tmp, path)
    except OSError as e:
        raise StorageError(f"Could not save contacts: {e}")


def clean_name(name):
    name = name.strip()
    if not name:
        raise ValueError("Name cannot be empty")
    return name


def clean_phone(phone):
    phone = phone.strip()
    digits = [c for c in phone if c.isdigit()]
    allowed = all(c.isdigit() or c in "+- " for c in phone)
    if not allowed or not 7 <= len(digits) <= 15:
        raise ValueError("Phone needs 7-15 digits (only digits, +, -, spaces)")
    return phone


def clean_email(email):
    email = email.strip()
    name, _, domain = email.partition("@")
    if (not name or "." not in domain or " " in email
            or "@" in domain or domain.startswith(".") or domain.endswith(".")):
        raise ValueError("Email not valid (example: name@mail.com)")
    return email


def find_contact(contacts, cid):
    for c in contacts:
        if c["id"] == cid:
            return c
    raise ValueError(f"No contact with id {cid}")


def add_contact(contacts, name, phone, email):
    new_id = max((c["id"] for c in contacts), default=0) + 1
    c = {"id": new_id, "name": clean_name(name),
         "phone": clean_phone(phone), "email": clean_email(email)}
    contacts.append(c)
    return c


def search_contacts(contacts, text):
    text = text.strip().lower()
    if not text:
        raise ValueError("Search text cannot be empty")
    return [c for c in contacts if text in c["name"].lower()]


def update_contact(contacts, cid, name="", phone="", email=""):
    c = find_contact(contacts, cid)
    new_name = clean_name(name) if name.strip() else c["name"]
    new_phone = clean_phone(phone) if phone.strip() else c["phone"]
    new_email = clean_email(email) if email.strip() else c["email"]
    c["name"], c["phone"], c["email"] = new_name, new_phone, new_email
    return c


def delete_contact(contacts, cid):
    c = find_contact(contacts, cid)
    contacts.remove(c)
    return c


def show_contacts(contacts):
    if not contacts:
        print("No contacts to show.")
        return
    print(f"{'ID':<5}{'Name':<20}{'Phone':<18}Email")
    for c in sorted(contacts, key=lambda x: x["id"]):
        print(f"{c['id']:<5}{c['name']:<20}{c['phone']:<18}{c['email']}")


def ask_for_id():
    try:
        return int(input("Contact ID: ").strip())
    except ValueError:
        raise ValueError("ID must be a whole number")


def main():
    try:
        contacts = load_contacts(CONTACTS_FILE)
    except StorageError as e:
        print("Problem:", e)
        return

    menu = ("\n1. Add contact\n2. Search by name\n3. Update contact\n"
            "4. Delete contact\n5. List all\n6. Exit")

    while True:
        print(menu)
        try:
            choice = input("Choose (1-6): ").strip()

            if choice == "1":
                c = add_contact(contacts, input("Name: "), input("Phone: "), input("Email: "))
                save_contacts(CONTACTS_FILE, contacts)
                print(f"Added contact with ID {c['id']}.")
            elif choice == "2":
                show_contacts(search_contacts(contacts, input("Search name: ")))
            elif choice == "3":
                cid = ask_for_id()
                find_contact(contacts, cid)
                print("Leave a field empty to keep old value.")
                update_contact(contacts, cid, input("New name: "),
                               input("New phone: "), input("New email: "))
                save_contacts(CONTACTS_FILE, contacts)
                print("Contact updated.")
            elif choice == "4":
                removed = delete_contact(contacts, ask_for_id())
                save_contacts(CONTACTS_FILE, contacts)
                print(f"Deleted {removed['name']}.")
            elif choice == "5":
                show_contacts(contacts)
            elif choice == "6":
                print("Bye!")
                break
            else:
                print("Please choose a number from 1 to 6.")
        except ValueError as e:
            print("Error:", e)
        except StorageError as e:
            print("Storage problem:", e)
        except EOFError:
            print("\nInput ended, closing.")
            break


if __name__ == "__main__":
    main()