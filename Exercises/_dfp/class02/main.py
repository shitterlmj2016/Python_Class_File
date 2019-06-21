
# def display_message():
#     print("hello class")

def display_message(message, times):
    print(message * times)

def get_message():
    return "Brian Kolowitz"

def get_address():
    street = "123 Fake Street"
    city = "Pittsburgh"
    state = "PA"
    zipcode = "15206"
    return street, city, state, zipcode

message = get_message()
display_message(message, 1)
display_message("hello class", 1)
display_message("this is the first lab", 3)
display_message("good luck", 2)

x = get_address()
print(type(x), x)

street, city, state, zipcode = get_address()
print(type(street), street, city, state, zipcode)
