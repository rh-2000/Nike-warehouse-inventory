
#========The beginning of the class==========
class Shoe(object):

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"


#=============Shoe list===========
shoe_list = []

#==========Functions outside the class==============
# using try-except-finally block to handle FileNotFoundErrors here
# this will be called in the other functions to ensure the file and the shoe_list are both synced
def read_shoes_data():
    file = None
    try:
        with open('inventory.txt', 'r') as file:
            for line in file.readlines():
                temp = line.strip().split(',')
                object = Shoe(temp[0],temp[1],temp[2],temp[3],temp[4])
                shoe_list.append(object)
            shoe_list.pop(0)
    except FileNotFoundError as error:
        print("The file you are trying to open does not exist.")
        print(error)
    finally:
        if file is not None:
            file.close()
        
def capture_shoes():
    print("\nADD NEW SHOE DATA\n")
    # creating user inputs to collect data for the object
    new_country = input("Country: ").capitalize()
    new_code = input("Code: ")
    new_product = input("Product: ").capitalize()
    # using try-except blocks for each of the integer inputs to handle ValueErrors
    while True:
        try:
            new_cost = int(input("Cost: £"))
            break
        except ValueError:
            print("Invalid input. Please enter whole number(s).")
    while True:
        try:
            new_quantity = int(input("Quantity (units): "))
            break
        except ValueError:
            print("Invalid input. Please enter whole number(s).")
    
    # appending new object to the list and also to the file
    # calling the read_shoes_data() so as not to overwrite the newly appended object when re-running the program
    # this wasn't specified in the task but it seems like an oversight to not do this
    new_object = Shoe(new_country,new_code,new_product,new_cost,new_quantity)
    shoe_list.append(new_object)
    with open('inventory.txt', 'a') as file:
        file.write(new_object)
    read_shoes_data()


def view_all():
    print("\nVIEW ALL SHOES\n")
    read_shoes_data()
    for item in shoe_list:
        print(item.__str__())

#
def re_stock():
    print("\nRE-STOCK\n")
    read_shoes_data()
    # storing all the quantities in a list to calculate the min value
    quantities = []
    for shoe in shoe_list:
        quantity = Shoe.get_quantity(shoe)
        quantities.append(int(quantity))
    lowest_quantity = min(quantities)

    # matching the lowest quantity to the object it belongs to here
    # creating and printing a new variable which holds the str value of the object
    # splitting this variable to be used in the next block
    for shoe in shoe_list:
        if str(lowest_quantity) == shoe.quantity:
            to_be_restocked = shoe.__str__()
            print("\nShoe to be restocked (lowest quantity):\n")
            print(to_be_restocked)
            temp = str(to_be_restocked).split(',')
    
    restock_choice = input("Would you like to restock these? (Y/N): ").upper()
    while True:
        if restock_choice == "Y":
            while True:
                try:
                    restock_qty = int(input("Enter the quantity you would like to restock: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a whole number.")
            with open('inventory.txt', 'r') as file:
                all_lines = []
                for lines in file.readlines():
                    line = lines.strip()
                    # checking the line being read matches the str value of the object with lowest qty
                    if line == str(to_be_restocked):
                        new_qty = int(line[-1]) + restock_qty
                        temp_line = line.split(',')
                        temp_line.pop(-1)
                        temp_line.append(str(new_qty))
                        new_line = ",".join(temp_line)
                        line = new_line
                    all_lines.append(line)
            # overwriting the entire file to include the new line contents
            with open('inventory.txt', 'w') as file:
                for line in all_lines:
                        file.write(f"{line}\n")
            print(f"The quantity has been updated.")
            read_shoes_data()
            break
        elif restock_choice == "N":
            break
        else:
            print("Invalid input. Please enter Y or N.")
            restock_choice = input("Would you like to restock these? (Y/N): ").upper()
            continue

# simple index of the iterated split lines to match the code string input by user
def search_shoe():
    print("\nSHOE SEARCH\n")
    read_shoes_data()
    input_code = input("Enter the code of the product you are looking for: ")
    with open('inventory.txt', 'r') as file:
        for lines in file.readlines():
            line = lines.strip()
            temp = line.split(',')
            if temp[1] == input_code:
                print(f"Details for shoe with code {input_code}:\n")
                print(line)
            else:
                print("Invalid code. Please try again.")


def value_per_item():
    print("\nVALUE PER ITEM\n")
    read_shoes_data()
    with open('inventory.txt', 'r') as file:
        for lines in file.readlines():
            line = lines.strip()
            # using this if statement to skip the first line of file
            if line == "Country,Code,Product,Cost,Quantity":
                pass
            else:
                temp = line.split(',')
                cost = int(temp[3])
                qty = int(temp[4])
                value = cost * qty
                print(f"\nTotal cost for product with code {temp[1]}:\t{value}")

# similar process to lowest quantity (re_stock() function) here
def highest_qty():
    print("\nITEM ON SALE\n")
    read_shoes_data()
    quantities = []
    for shoe in shoe_list:
        quantity = Shoe.get_quantity(shoe)
        quantities.append(int(quantity))
    highest_quantity = max(quantities)

    for shoe in shoe_list:
        if str(highest_quantity) == shoe.quantity:
            print("\nShoe with the highest quantity:\n")
            print(shoe.__str__())
            print("\nThis item has been put on sale.")

#==========Main Menu=============

# set up menu in a while loop to continue until user inputs to exit
while True:
    menu = (f'''\nMENU\nPlease select from the following:\n
    a = add shoe data
    va = view all shoes
    r = restock an item
    s = search for a shoe
    vpi = view value per item
    os = put an item on sale
    e = exit
    ''')
    print(menu)
    menu_choice = input("Choice: ").lower()

    if menu_choice == "a":
        capture_shoes()
    elif menu_choice == "va":
        view_all()
    elif menu_choice == "r":
        re_stock()
    elif menu_choice == "s":
        search_shoe()
    elif menu_choice == "vpi":
        value_per_item()
    elif menu_choice == "os":
        highest_qty()
    elif menu_choice == "e":
        print("Exiting.")
        break
    else:
        print("Invalid input. Please try again.")