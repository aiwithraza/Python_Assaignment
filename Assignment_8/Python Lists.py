# Q1
numbers = [10,20,30,40,50,60,70]
first = numbers[0]
middle = numbers[len(numbers)//2]
last = numbers[-1]
print(first, middle, last)


# Q2
numbers = [5,10,15,20,25,30,35,40,45,50]
first_five = numbers[:5]
last_four = numbers[-4:]
every_second_reverse = numbers[::-2]
print(first_five)
print(last_four)
print(every_second_reverse)


# Q3
fruits = ["apple","banana","cherry","mango"]
fruits[fruits.index("banana")] = "orange"
fruits.insert(2, "grapes")
fruits.remove("cherry")
print(fruits)


# Q4
numbers = [12,45,23,67,89,34]
reversed_list = numbers[::-1]
print(reversed_list)
print(numbers)


# Q5
numbers = [45,12,89,34,89,67,45,23]
unique_sorted = sorted(set(numbers), reverse=True)
second_largest = unique_sorted[1]
print(second_largest)


# Q6
numbers = [10,20,30,40,50,60]
k = 2
rotated = numbers[-k:] + numbers[:-k]
print(rotated)


# Q7
numbers = [10,20,10,30,20,40,30,50]
unique_list = list(dict.fromkeys(numbers))
print(unique_list)


# Q8
data = [[10,20],[30,40],[50,60]]
flattened = data[0] + data[1] + data[2]
print(flattened)


# Q9
matrix = [[10,20,30],[40,50,60],[70,80,90]]
main_diagonal = [matrix[0][0], matrix[1][1], matrix[2][2]]
secondary_diagonal = [matrix[0][2], matrix[1][1], matrix[2][0]]
middle_column = [matrix[0][1], matrix[1][1], matrix[2][1]]
print(main_diagonal, sum(main_diagonal))
print(secondary_diagonal, sum(secondary_diagonal))
print(middle_column, sum(middle_column))


# Q10
data = [15,5,25,10,35,20,30]
unique_sorted = sorted(set(data))
three_largest = unique_sorted[-3:]
two_smallest = unique_sorted[:2][::-1]
result = three_largest + two_smallest
print(result)