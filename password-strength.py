password = input("Password: ")
lower = 0
upper = 0
symbol = 0
number = 0
length = len(password)
rating = 0

for char in password:
    if char.isdigit():
        number += 1
    elif char.isalpha():
        if char.islower():
            lower += 1
        elif char.isupper():
            upper += 1
    else:
        symbol += 1

print("lower: ", lower)
print("upper: ", upper)
print("symbol: ", symbol)
print("number: ", number)

if length > 8:
    rating += 10
rating += upper * 10 / (upper**2 / 1.2)

print(rating)
