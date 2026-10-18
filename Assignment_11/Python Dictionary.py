# Q31
student = {"name": "Ali", "age": 22, "course": "Python", "marks": 85}
name = student["name"]
marks = student["marks"]
city = student.get("city", "Karachi")
print(name)
print(marks)
print(city)


# Q32
employee = {"name": "Sara", "salary": 100000, "department": "IT"}
employee["salary"] = employee["salary"] + (employee["salary"] * 20 / 100)
employee["bonus"] = 15000
employee["department"] = "Data Engineering"
print(employee)


# Q33
product = {"id": 101, "name": "Laptop", "price": 120000, "stock": 5}
keys = product.keys()
values = product.values()
items = product.items()
stock_value = product.pop("stock")
print(keys)
print(values)
print(items)
print(stock_value)
print(product)


# Q34
dict1 = {"a": 10, "b": 20, "c": 30}
dict2 = {"b": 50, "d": 40}
merged = dict1 | dict2
print(merged)


# Q35
marks = {"Ali": 85, "Sara": 92, "Ahmed": 78, "Zain": 88}
highest = max(marks.values())
lowest = min(marks.values())
average = sum(marks.values()) / len(marks)
top_student = max(marks, key=marks.get)
print(highest)
print(lowest)
print(average)
print(top_student)


# Q36
employees = {
    "E101": {"name": "Ali", "salary": 80000},
    "E102": {"name": "Sara", "salary": 120000},
    "E103": {"name": "Ahmed", "salary": 95000}
}
sara_salary = employees["E102"]["salary"]
employees["E101"]["salary"] = employees["E101"]["salary"] + (employees["E101"]["salary"] * 15 / 100)
total_payroll = employees["E101"]["salary"] + employees["E102"]["salary"] + employees["E103"]["salary"]
print(sara_salary)
print(employees["E101"]["salary"])
print(total_payroll)


# Q37
data = {"Python": "Ali", "SQL": "Sara", "AWS": "Ahmed"}
inverse = dict(zip(data.values(), data.keys()))
print(inverse)


# Q38
order = {
    "laptop": {"price": 120000, "quantity": 2},
    "mouse": {"price": 1500, "quantity": 5},
    "keyboard": {"price": 3500, "quantity": 3}
}
laptop_subtotal = order["laptop"]["price"] * order["laptop"]["quantity"]
mouse_subtotal = order["mouse"]["price"] * order["mouse"]["quantity"]
keyboard_subtotal = order["keyboard"]["price"] * order["keyboard"]["quantity"]
grand_total = laptop_subtotal + mouse_subtotal + keyboard_subtotal
after_discount = grand_total - (grand_total * 10 / 100)
print(laptop_subtotal)
print(mouse_subtotal)
print(keyboard_subtotal)
print(grand_total)
print(after_discount)


# Q39
employees = {
    "Ali": {"python": 90, "sql": 85, "aws": 88},
    "Sara": {"python": 95, "sql": 92, "aws": 90},
    "Ahmed": {"python": 80, "sql": 87, "aws": 84}
}
ali_avg = sum(employees["Ali"].values()) / len(employees["Ali"])
sara_avg = sum(employees["Sara"].values()) / len(employees["Sara"])
ahmed_avg = sum(employees["Ahmed"].values()) / len(employees["Ahmed"])
top_performer = max(employees, key=lambda x: sum(employees[x].values()) / len(employees[x]))
highest_sql = max(employees, key=lambda x: employees[x]["sql"])
print(ali_avg)
print(sara_avg)
print(ahmed_avg)
print(top_performer)
print(highest_sql)


# Q40
inventory = {
    "P101": {"name": "Laptop", "price": 120000, "stock": 5},
    "P102": {"name": "Mouse", "price": 1500, "stock": 20},
    "P103": {"name": "Keyboard", "price": 3500, "stock": 10}
}
total_value = (
    inventory["P101"]["price"] * inventory["P101"]["stock"] +
    inventory["P102"]["price"] * inventory["P102"]["stock"] +
    inventory["P103"]["price"] * inventory["P103"]["stock"]
)
most_valuable = max(inventory, key=lambda x: inventory[x]["price"] * inventory[x]["stock"])
inventory["P101"]["stock"] = inventory["P101"]["stock"] - 2
inventory["P102"]["stock"] = inventory["P102"]["stock"] - 5
print(total_value)
print(most_valuable)
print(inventory["P101"]["stock"])
print(inventory["P102"]["stock"])