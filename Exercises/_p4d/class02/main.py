def add(a, b):
    return a + b 

def get_greeting():
    return "Hello Class"

def get_address():
    street = "123 fake street"
    city = "Pittsburgh"
    zip_code = 15206
    return street, city, zip_code

def count_to_10():
    for i in range(11):
        print(i)

result = add(3, 7)

print(type(result), result)

greeting = get_greeting()
print(type(greeting), greeting)

x = get_address()
print(type(x), x)

street, city, zip_code = get_address()
print(type(street), type(city), type(zip_code), street, city, zip_code)

result = count_to_10()
if result == None:
    print('didn\'t return anything')
print(type(result), result)