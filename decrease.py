query="Decrease the volume by 200"
numbers = []
current_number = ""
for char in query:
    if char.isnumeric():
        current_number += char
    else:
        if current_number:
            numbers.append(int(current_number))
            current_number = ""
if current_number:
    numbers.append(int(current_number))
print(current_number)