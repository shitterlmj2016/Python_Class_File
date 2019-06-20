import os

def print_menu():
    print("Options")
    print("1. to print welcome message")
    print("2. to print course description")
    print("3. load file and print")
    print("q. to quit")

def welcome_message():
    print('hello class')

def course_description():
    print('this is an introduction to python')

def load_file_and_print(top=3):
    file_name = '/Users/kolobj/Google Drive/Python/Exercises/console/test.csv'
    with open(file_name, 'r') as f:
        for index, line in enumerate(f):
            if index >= top:
                break
            print(line)



def handle_menu_options(menu_item):
    if menu_item == 1:
        welcome_message()
    elif menu_item == 2:
        course_description()
    elif menu_item == 3:
        load_file_and_print(1)
    else:
        print('invalid option', menu_item)

def go():
    while True:
        print_menu()
        option = input("select an option> ")
        if option == 'q':
            break

        try:
            menu_item = int(option)            
            handle_menu_options(menu_item)
        except ValueError as e:
            print('ValueError', e)
        except Exception as e:
            print('Exception', e)


if __name__ == "__main__":
    go()