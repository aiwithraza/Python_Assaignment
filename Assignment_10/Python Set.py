# Q21
numbers = [10,20,10,30,40,20,50]
unique_set = set(numbers)
print(unique_set)
print(len(unique_set))


# Q22
a = {1,2,3,4,5}
b = {4,5,6,7,8}
print(a | b)
print(a & b)
print(a - b)
print(a ^ b)


# Q23
skills = {"Python","SQL","AWS"}
skills.add("Snowflake")
skills.add("Databricks")
skills.discard("AWS")
print(skills)


# Q24
python_students = {"Ali","Sara","Ahmed","Zain"}
sql_students = {"Sara","Ahmed","Hamza","Usman"}
both = python_students & sql_students
exactly_one = python_students ^ sql_students
print(both)
print(exactly_one)


# Q25
required_skills = {"Python","SQL"}
candidate_skills = {"Python","SQL","AWS","Snowflake"}
print(required_skills.issubset(candidate_skills))
print(candidate_skills.issuperset(required_skills))


# Q26
numbers = {1,2,4,6,8,10}
all_numbers = set(range(1, 11))
missing = all_numbers - numbers
print(missing)


# Q27
python = {"Ali","Sara","Ahmed","Zain"}
sql = {"Sara","Ahmed","Hamza"}
aws = {"Ahmed","Zain","Hamza"}
all_three = python & sql & aws
exactly_py_sql = (python & sql) - aws
at_least_two = (python & sql) | (python & aws) | (sql & aws)
print(all_three)
print(exactly_py_sql)
print(at_least_two)


# Q28
day1 = {101, 102, 103, 104}
day2 = {103, 104, 105, 106}
day3 = {104, 106, 107, 108}
all_days = day1 & day2 & day3
exactly_one = (day1 ^ day2 ^ day3) - ((day1 & day2) | (day1 & day3) | (day2 & day3))
at_least_two = (day1 & day2) | (day1 & day3) | (day2 & day3)
print(all_days)
print(exactly_one)
print(at_least_two)


# Q29
required_permissions = {"read", "write", "execute"}
user_permissions = {"read", "write", "delete"}
missing = required_permissions - user_permissions
extra = user_permissions - required_permissions
full_auth = required_permissions.issubset(user_permissions)
print(missing)
print(extra)
print(full_auth)


# Q30
website = {"C1", "C2", "C3", "C4", "C5"}
mobile = {"C3", "C4", "C6", "C7"}
store = {"C2", "C4", "C7", "C8"}
exactly_one = (website ^ mobile ^ store) - ((website & mobile) | (website & store) | (mobile & store))
exactly_two = ((website & mobile) | (website & store) | (mobile & store)) - (website & mobile & store)
all_three = website & mobile & store
print(exactly_one)
print(exactly_two)
print(all_three)