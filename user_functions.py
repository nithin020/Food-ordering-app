import csv
import os
import re
from pathlib import Path
import datetime

from constants.constant import user_database, food_database, resources


class UserFunctions:
    """
    This class handles user-related functionality, including user registration, login, placing orders,
    updating user profile, and managing order history.
    """
    def __init__(self):
        """
        Initialize the UserFunctions class by setting the paths to user and food databases.
        """
        self.root = Path(__file__).parent.parent
        self.user_csv_path = os.path.join(self.root, resources, user_database)
        self.food_csv_path = os.path.join(self.root, resources, food_database)

    def user(self, app):
        """
        Display the user login screen and handle user choices for login, registration, or going back.

        Parameters:
            app (object): An instance of the main application class.

        """
        print("***User login screen***")
        print("1. Login")
        print("2. Register")
        print("3. Go Back")

        choice = input("Please enter your choice: ")

        if choice == "1":
            self.login_user(app)
        elif choice == "2":
            self.register_user(app)
        elif choice == "3":
            app.welcome_screen()
        else:
            print("Invalid choice. Please try again.")
            self.user(app)

    def register_user(self, app):
        """
        Register a new user by collecting user information and saving it to the user database.

        Parameters:
            app (object): An instance of the main application class.

        """
        print("***User Registration***")
        full_name = input("Enter your full name: ")
        phone_number = input("Enter your phone number: ")
        email = input("Enter your email: ")
        address = input("Enter your address: ")
        password = input("Enter your password: ")

        if not self.validate_phone_number(phone_number):
            print("Invalid phone number. Please enter a 10-digit phone number.")
            self.user(app)
            return

        if not self.validate_email(email):
            print("Invalid email address. Please enter a valid email.")
            self.user(app)
            return

        if not self.validate_password(password):
            print("Invalid password. Please enter a password with at least 8 characters.")
            self.user(app)
            return

        user_data = {
            "Full Name": full_name,
            "Phone Number": phone_number,
            "Email": email,
            "Address": address,
            "Password": password
        }
        self.save_user_data(user_data)

        print("Registration successful! Please proceed to login.")
        self.user(app)

    def save_user_data(self, user_data):
        """
        Save the user data to the user database.

        Parameters:
            user_data (dict): A dictionary containing user information.

        """
        with open(self.user_csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(user_data.values())

    def login_user(self, app):
        """
        Handle the user login process by verifying user credentials.

        Parameters:
            app (object): An instance of the main application class.

        """
        print("***User Login***")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        if self.verify_user(email, password):
            print("Login successful!")
            self.user_menu(app, email)
        else:
            print("Invalid email or password. Please try again.")
            self.user(app)

    def verify_user(self, email, password):
        """
        Verify the user's credentials by checking if they exist in the user database.

        Parameters:
            email (str): User's email address.
            password (str): User's password.

        Returns:
            bool: True if the user's credentials are valid, False otherwise.

        """
        with open(self.user_csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Email"] == email and row["Password"] == password:
                    return True
        return False

    def validate_phone_number(self, phone_number):
        """
        Validate a phone number by checking if it has 10 digits.

        Parameters:
            phone_number (str): The phone number to validate.

        Returns:
            bool: True if the phone number is valid, False otherwise.

        """
        return len(phone_number) == 10 and phone_number.isdigit()

    def validate_email(self, email):
        """
        Validate an email address by checking if it has a valid format.

        Parameters:
            email (str): The email address to validate.

        Returns:
            bool: True if the email address is valid, False otherwise.

        """
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, email)

    def validate_password(self, password):
        """
        Validate a password by checking if it has at least 8 characters.

        Parameters:
            password (str): The password to validate.

        Returns:
            bool: True if the password is valid, False otherwise.

        """
        return len(password) >= 8

    def user_menu(self, app, email):
        """
        Display the user menu and handle user choices for placing orders, updating profile, or logging out.

        Parameters:
            app (object): An instance of the main application class.
            :param email: email of the user

        """
        print("***User Menu***")
        print("1. Place New Order")
        print("2. Order History")
        print("3. Update Profile")
        print("4. Logout")

        choice = input("Please enter your choice: ")

        if choice == "1":
            self.place_order(app, email)
        elif choice == "2":
            self.order_history(app, email)
        elif choice == "3":
            self.update_profile(app)
        elif choice == "4":
            app.welcome_screen()
        else:
            print("Invalid choice. Please try again.")
            self.user_menu(app, email)

    def place_order(self, app, email):
        """
        Place a food order by selecting items from the menu and saving the order details.

        Parameters:
            app (object): An instance of the main application class.
            :param email: email of the user

        """
        print("*Place New Order*")
        food_list = self.load_food_items()
        print("Food List:")

        for index, food_item in enumerate(food_list, start=1):
            print(
                f"{index}.  {food_item['name']} ({food_item['stock']}/{food_item['quantity']}) [INR {food_item['price']}]")

        choice = input("Enter the index of the food item to order (or enter '0' to go back): ")

        if choice == "0":
            self.user_menu(app, email)
            return

        if not choice.isdigit() or int(choice) <= 0 or int(choice) > len(food_list):
            print("Invalid choice. Please enter a valid index.")
            self.place_order(app, email)
            return

        chosen_food = food_list[int(choice) - 1]
        max_quantity = int(chosen_food['stock'])

        quantity = input(f"Enter the quantity you want to order (1-{max_quantity}): ")
        if not quantity.isdigit() or int(quantity) <= 0 or int(quantity) > max_quantity:
            print("Invalid quantity. Please enter a valid quantity.")
            self.place_order(app, email)
            return

        print(f"You have chosen {quantity} {chosen_food['name']}.")

        if int(quantity) > int(chosen_food['stock']):
            print(f"Insufficient stock. The available stock for {chosen_food['name']} is {chosen_food['stock']}. "
                  f"Please choose a lower quantity.")
            self.place_order(app, email)
            return

        print("1. Confirm Order")
        print("2. Go Back")

        confirm_choice = input("Enter your choice: ")

        if confirm_choice == "1":
            email = input("Enter your email: ")
            self.order_food(app, chosen_food, email, quantity)
        elif confirm_choice == "2":
            self.place_order(app, email)
        else:
            print("Invalid choice. Please try again.")
            self.place_order(app, email)

    def load_food_items(self):
        """
        Loads the food items from a CSV file and returns a list of dictionaries representing the food items.

        Returns:
            list: A list of dictionaries representing the food items.
        """
        food_items = []
        with open(self.food_csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                stock_value = row['stock']
                stock_value = ''.join(filter(str.isdigit, stock_value))
                row['stock'] = stock_value
                food_items.append(row)
        return food_items

    def update_food_item(self, food_item):
        """
        Updates a food item in the CSV file with the provided food item data.

        Args:
            food_item (dict): The updated food item data.

        """
        food_items = self.load_food_items()

        index = None
        for i, item in enumerate(food_items):
            if item['food_id'] == food_item['food_id']:
                index = i
                break

        if index is not None:
            food_items[index] = food_item

            with open(self.food_csv_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=food_items[0].keys())
                writer.writeheader()
                writer.writerows(food_items)

    def order_food(self, app, food_item, email, quantity):
        """
        Places an order for the specified food item and adds it to the order history.

        Args:
            app (object): An instance of the main application class.
            food_item (dict): The food item to order.
            email (str): The email of the user placing the order.
            :param quantity: The quantity of the user placing order

        """
        available_stock = int(food_item['stock'])
        if available_stock < int(quantity):
            print(f"Insufficient stock. The available stock for {food_item['name']} is {available_stock}. "
                  f"Please choose a lower quantity.")
            return

        print(f"Order confirmed for {quantity} {food_item['name']} INR {food_item['price']} each.")
        food_item['stock'] = str(available_stock - int(quantity))
        self.update_food_item(food_item)
        self.add_order_to_history(food_item, email)
        print("Order placed successfully!")
        self.user_menu(app, email)

    def add_order_to_history(self, food_item, email):
        """
        Adds an order to the user's order history in the CSV file.

        Args:
            food_item (dict): The food item that was ordered.
            email (str): The email of the user placing the order.

        """
        now = datetime.datetime.now()
        order_data = {
            "Food Name": food_item['name'],
            "Price": food_item['price'],
            "Order Date": str(now.strftime("%Y-%m-%d %H:%M:%S"))
        }

        with open(self.user_csv_path, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        for row in rows:
            if row["Email"] == email:
                if row.get("Order History"):
                    row[
                        "Order History"] += f"\n Food: {order_data['Food Name']} - INR {order_data['Price']} - Order date: {order_data['Order Date']}"
                else:
                    row[
                        "Order History"] = f"Food: {order_data['Food Name']} - INR {order_data['Price']} - Order date: {order_data['Order Date']}"
                break

        with open(self.user_csv_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    def order_history(self, app, email):
        """
        Displays the order history for a user based on their email.

        Args:
            app: The application or context in which the order history is being displayed.
            email (str): The email of the user.
        """
        print("*Order History*")
        with open(self.user_csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Email"] == email:
                    if "Order History" in row:
                        order_history = row["Order History"]
                        orders = order_history.split("\n")
                        for order in orders:
                            print(order)
                    else:
                        print("No order history found.")
                    break
        self.user_menu(app, email)

    def update_profile(self, app):
        """
        Update user profile information by allowing users to modify their details.

        Parameters:
            app (object): An instance of the main application class.

        """
        print("Update Profile")
        email = input("Enter your email: ")
        new_data = {}

        with open(self.user_csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Email"] == email:
                    new_data = self.get_updated_user_data(row)
                    break

        if not new_data:
            print("User not found. Please try again.")
            self.user_menu(app, email)
            return

        updated_rows = []
        with open(self.user_csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Email"] == email:
                    row.update(new_data)
                updated_rows.append(row)

        with open(self.user_csv_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=updated_rows[0].keys())
            writer.writeheader()
            writer.writerows(updated_rows)

        print("Profile updated successfully!")
        self.user_menu(app, email)

    def get_updated_user_data(self, user_data):
        """
        Prompts the user to enter new profile information and returns the updated user data.

        Args:
            user_data (dict): The current user data containing profile information.

        Returns:
            dict: The updated user data with any changes made by the user.

        """

        new_data = {}
        print("Enter new profile information (leave blank for no change):")

        full_name = input(f"Full Name ({user_data['Full Name']}): ").strip()
        new_data["Full Name"] = full_name if full_name else user_data["Full Name"]

        phone_number = input(f"Phone Number ({user_data['Phone Number']}): ").strip()
        if phone_number:
            if not self.validate_phone_number(phone_number):
                print("Invalid phone number. Profile update failed.")
                return {}
            new_data["Phone Number"] = phone_number
        else:
            new_data["Phone Number"] = user_data["Phone Number"]

        address = input(f"Address ({user_data['Address']}): ").strip()
        new_data["Address"] = address if address else user_data["Address"]

        return new_data


user_functions = UserFunctions()
