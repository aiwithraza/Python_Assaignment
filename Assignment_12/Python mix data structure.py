# Q41
students = (
    {"id": 1, "name": "Ali", "marks": (85, 90, 88)},
    {"id": 2, "name": "Sara", "marks": (92, 95, 91)},
    {"id": 3, "name": "Ahmed", "marks": (78, 84, 80)}
)
ali_avg = sum(students[0]["marks"]) / len(students[0]["marks"])
sara_avg = sum(students[1]["marks"]) / len(students[1]["marks"])
ahmed_avg = sum(students[2]["marks"]) / len(students[2]["marks"])
top_student = max(students, key=lambda x: sum(x["marks"]))
names = (students[0]["name"], students[1]["name"], students[2]["name"])
all_marks = students[0]["marks"] + students[1]["marks"] + students[2]["marks"]
unique_marks = set(all_marks)
print(ali_avg)
print(sara_avg)
print(ahmed_avg)
print(top_student)
print(names)
print(unique_marks)


# Q42
employees = {
    "Ali": {"Python", "SQL", "AWS"},
    "Sara": {"Python", "Databricks", "SQL"},
    "Ahmed": {"AWS", "Snowflake", "SQL"}
}
common_skills = employees["Ali"] & employees["Sara"] & employees["Ahmed"]
ali_only = employees["Ali"] - employees["Sara"] - employees["Ahmed"]
all_skills = employees["Ali"] | employees["Sara"] | employees["Ahmed"]
python_sql = {"Python", "SQL"}
qualified = tuple(name for name in employees if python_sql.issubset(employees[name]))
print(common_skills)
print(ali_only)
print(all_skills)
print(qualified)


# Q43
sales = {
    ("Laptop", 120000, 2),
    ("Mouse", 1500, 5),
    ("Keyboard", 3500, 3)
}
revenues = {item[0]: item[1] * item[2] for item in sales}
total_revenue = sum(revenues.values())
top_product = max(revenues, key=revenues.get)
prices = {item[1] for item in sales}
print(total_revenue)
print(top_product)
print(revenues)
print(prices)


# Q44
customers = {
    "C101": {"name": "Ali", "orders": [1200, 2500, 1800]},
    "C102": {"name": "Sara", "orders": [3000, 4500]},
    "C103": {"name": "Ahmed", "orders": [1500, 2000, 1000]}
}
ali_total = sum(customers["C101"]["orders"])
sara_total = sum(customers["C102"]["orders"])
ahmed_total = sum(customers["C103"]["orders"])
totals = {"C101": ali_total, "C102": sara_total, "C103": ahmed_total}
top_customer = max(totals, key=totals.get)
totals_tuple = (ali_total, sara_total, ahmed_total)
print(ali_total)
print(sara_total)
print(ahmed_total)
print(top_customer)
print(totals_tuple)


# Q45
courses = {
    "Python": {"Ali", "Sara", "Ahmed"},
    "SQL": {"Sara", "Ahmed", "Zain"},
    "AWS": {"Ali", "Ahmed", "Zain"}
}
all_three = courses["Python"] & courses["SQL"] & courses["AWS"]
exactly_two = (
    (courses["Python"] & courses["SQL"]) |
    (courses["Python"] & courses["AWS"]) |
    (courses["SQL"] & courses["AWS"])
) - all_three
exactly_one = (
    (courses["Python"] ^ courses["SQL"] ^ courses["AWS"]) -
    ((courses["Python"] & courses["SQL"]) |
     (courses["Python"] & courses["AWS"]) |
     (courses["SQL"] & courses["AWS"]))
)
unique_students = courses["Python"] | courses["SQL"] | courses["AWS"]
print(exactly_two)
print(all_three)
print(exactly_one)
print(len(unique_students))


# Q46
transactions = (
    {"id": 101, "customer": "Ali", "items": [("Laptop", 120000, 1), ("Mouse", 1500, 2)]},
    {"id": 102, "customer": "Sara", "items": [("Keyboard", 3500, 2), ("Mouse", 1500, 1)]},
    {"id": 103, "customer": "Ali", "items": [("Monitor", 45000, 1)]}
)
t1_total = transactions[0]["items"][0][1] * transactions[0]["items"][0][2] + transactions[0]["items"][1][1] * transactions[0]["items"][1][2]
t2_total = transactions[1]["items"][0][1] * transactions[1]["items"][0][2] + transactions[1]["items"][1][1] * transactions[1]["items"][1][2]
t3_total = transactions[2]["items"][0][1] * transactions[2]["items"][0][2]
total_revenue = t1_total + t2_total + t3_total
ali_spending = t1_total + t3_total
largest_transaction = max(t1_total, t2_total, t3_total)
unique_products = {transactions[0]["items"][0][0], transactions[0]["items"][1][0], transactions[1]["items"][0][0], transactions[1]["items"][1][0], transactions[2]["items"][0][0]}
print(total_revenue)
print(ali_spending)
print(largest_transaction)
print(unique_products)


# Q47
pipelines = {
    "pipeline_1": {"status": "success", "records": (1000, 1200, 1100)},
    "pipeline_2": {"status": "failed", "records": (800, 0, 0)},
    "pipeline_3": {"status": "success", "records": (1500, 1600, 1700)}
}
p1_total = sum(pipelines["pipeline_1"]["records"])
p2_total = sum(pipelines["pipeline_2"]["records"])
p3_total = sum(pipelines["pipeline_3"]["records"])
total_processed = p1_total + p2_total + p3_total
failed_pipelines = tuple(k for k in pipelines if pipelines[k]["status"] == "failed")
largest_pipeline = max(p1_total, p2_total, p3_total)
p1_avg = p1_total / len(pipelines["pipeline_1"]["records"])
p2_avg = p2_total / len(pipelines["pipeline_2"]["records"])
p3_avg = p3_total / len(pipelines["pipeline_3"]["records"])
print(total_processed)
print(failed_pipelines)
print(largest_pipeline)
print(p1_avg, p2_avg, p3_avg)


# Q48
accounts = {
    "A101": {"holder": "Ali", "transactions": [5000, -2000, 3000, -1000]},
    "A102": {"holder": "Sara", "transactions": [10000, -3000, -2000]},
    "A103": {"holder": "Ahmed", "transactions": [7000, -1500, 2500]}
}
a101_balance = sum(accounts["A101"]["transactions"])
a102_balance = sum(accounts["A102"]["transactions"])
a103_balance = sum(accounts["A103"]["transactions"])
highest_balance = max(a101_balance, a102_balance, a103_balance)
total_withdrawals = abs(sum(x for x in accounts["A101"]["transactions"] if x < 0)) + abs(sum(x for x in accounts["A102"]["transactions"] if x < 0)) + abs(sum(x for x in accounts["A103"]["transactions"] if x < 0))
largest_deposit = max(max(accounts["A101"]["transactions"]), max(accounts["A102"]["transactions"]), max(accounts["A103"]["transactions"]))
print(a101_balance, a102_balance, a103_balance)
print(highest_balance)
print(total_withdrawals)
print(largest_deposit)


# Q49
users = {
    "Ali": {"purchased": {"Laptop", "Mouse"}, "wishlist": {"Keyboard", "Monitor", "Mouse"}},
    "Sara": {"purchased": {"Keyboard", "Monitor"}, "wishlist": {"Laptop", "Mouse"}},
    "Ahmed": {"purchased": {"Laptop", "Keyboard"}, "wishlist": {"Monitor", "Headphones"}}
}
bought_at_least_two = (
    (users["Ali"]["purchased"] & users["Sara"]["purchased"]) |
    (users["Ali"]["purchased"] & users["Ahmed"]["purchased"]) |
    (users["Sara"]["purchased"] & users["Ahmed"]["purchased"])
)
ali_wishlist_minus = users["Ali"]["wishlist"] - users["Ali"]["purchased"]
shared_wishlist = users["Ali"]["wishlist"] & users["Sara"]["wishlist"] & users["Ahmed"]["wishlist"]
all_products = users["Ali"]["purchased"] | users["Ali"]["wishlist"] | users["Sara"]["purchased"] | users["Sara"]["wishlist"] | users["Ahmed"]["purchased"] | users["Ahmed"]["wishlist"]
print(bought_at_least_two)
print(ali_wishlist_minus)
print(shared_wishlist)
print(all_products)


# Q50
company = {
    "departments": {
        "Engineering": {
            "employees": {
                ("Ali", 120000, {"Python", "AWS", "SQL"}),
                ("Sara", 150000, {"Python", "Databricks", "SQL"})
            },
            "budget": 500000
        },
        "Analytics": {
            "employees": {
                ("Ahmed", 100000, {"SQL", "Power BI"}),
                ("Zain", 130000, {"Python", "SQL", "Tableau"})
            },
            "budget": 400000
        }
    }
}
eng_employees = company["departments"]["Engineering"]["employees"]
ana_employees = company["departments"]["Analytics"]["employees"]
eng_payroll = sum(e[1] for e in eng_employees)
ana_payroll = sum(e[1] for e in ana_employees)
total_payroll = eng_payroll + ana_payroll
highest_paid = max(list(eng_employees) + list(ana_employees), key=lambda x: x[1])
eng_skills = set.union(*[e[2] for e in eng_employees])
ana_skills = set.union(*[e[2] for e in ana_employees])
common_skills = eng_skills & ana_skills
eng_only_skills = eng_skills - ana_skills
eng_remaining = company["departments"]["Engineering"]["budget"] - eng_payroll
ana_remaining = company["departments"]["Analytics"]["budget"] - ana_payroll
eng_avg = eng_payroll / len(eng_employees)
ana_avg = ana_payroll / len(ana_employees)
higher_avg = "Engineering" if eng_avg > ana_avg else "Analytics"
name_to_salary = {e[0]: e[1] for e in list(eng_employees) + list(ana_employees)}
combined_budget = company["departments"]["Engineering"]["budget"] + company["departments"]["Analytics"]["budget"]
sufficient = combined_budget >= total_payroll
print(eng_payroll)
print(total_payroll)
print(highest_paid)
print(common_skills)
print(eng_only_skills)
print(eng_remaining, ana_remaining)
print(higher_avg)
print(name_to_salary)
print(sufficient)