# Q11
colors = ("red", "green", "blue", "yellow", "purple")
second = colors[1]
last = colors[-1]
middle_three = colors[1:4]
print(second)
print(last)
print(middle_three)


# Q12
employee = ("Ali", 28, "Data Engineer", 150000)
name, age, role, salary = employee
print(name)
print(salary)


# Q13
tuple1 = (10,20,30)
tuple2 = (40,50,60)
combined = tuple1 + tuple2
reversed_tuple = combined[::-1]
print(combined)
print(reversed_tuple)


# Q14
numbers = (10,20,30,20,40,20,50)
count_20 = numbers.count(20)
first_index = numbers.index(20)
print(count_20)
print(first_index)


# Q15
data = (100,200,300,400,500,600)
first, second, *remaining, last = data
print(first)
print(second)
print(last)
print(remaining)


# Q16
numbers = (10,20,30,40,50)
index_30 = numbers.index(30)
new_tuple = numbers[:index_30] + (300,) + numbers[index_30+1:]
print(new_tuple)


# Q17
students = (
    ("Ali", (85, 90, 88)),
    ("Sara", (92, 87, 95)),
    ("Ahmed", (78, 84, 80))
)
sara_second = students[1][1][1]
ali_avg = sum(students[0][1]) / len(students[0][1])
ahmed_highest = max(students[2][1])
print(sara_second)
print(ali_avg)
print(ahmed_highest)


# Q18
employees = (
    ("Ali", 80000),
    ("Sara", 120000),
    ("Ahmed", 95000)
)
sorted_employees = tuple(sorted(employees, key=lambda x: x[1], reverse=True))
print(sorted_employees)


# Q19
matrix = ((2, 4, 6), (8, 10, 12), (14, 16, 18))
diagonal = (matrix[0][0], matrix[1][1], matrix[2][2])
product = matrix[0][0] * matrix[1][1] * matrix[2][2]
row_sums = (sum(matrix[0]), sum(matrix[1]), sum(matrix[2]))
print(diagonal)
print(product)
print(row_sums)


# Q20
records = (
    ("Laptop", 120000, 5),
    ("Mouse", 1500, 20),
    ("Keyboard", 3500, 10)
)
inventory_value = (
    records[0][1] * records[0][2] +
    records[1][1] * records[1][2] +
    records[2][1] * records[2][2]
)
most_expensive = max(records, key=lambda x: x[1])
reversed_names = (records[2][0], records[1][0], records[0][0])
print(inventory_value)
print(most_expensive)
print(reversed_names)