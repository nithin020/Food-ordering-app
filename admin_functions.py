import csv
import os
from pathlib import Path
import random

from constants.constant import admin_credentials, food_database, five_digit_low, five_digit_high, resources


class AdminFunctions:
    """
    Class that provides admin functionality for the Food Delivery App.
    """
    root = Path(__file__).parent.parent
    admin_csv_path = os.path.join(root, resources, admin_credentials)
    food_csv_path = os.path.join(root, resources, food_database)

    def __init__(self):
        """
        Initializes the AdminFunctions class.
        """
        self.users = self.load_users()

    def admin(self, app):
        """
        Displays the admin login screen and handles the admin login process.

        Args:
            app: The FoodDeliveryApp instance.

        """
        print("***Admin login screen***")
        print("1. Login")
        print("2. Go back")

        choice = input("Please enter your choice: ")

        if choice == "1":
            user_id = input("Enter your user ID: ")
            password = input("Enter your password: ")

            if self.verify_user(user_id, password):
                print("Login successful!")
                self.admin_authority(app)
            else:
                print("Invalid user ID or password. Please try again.")
                self.admin(app)
        elif choice == "2":
            app.welcome_screen()
        else:
            print("Invalid choice. Please try again.")
            self.admin(app)

    def load_users(self):
        """
        Loads the admin users from the admin CSV file.

        Returns:
            A list of admin users.

        """
        users = []
        with open(self.admin_csv_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                users.append({'user_id': row[0], 'password': row[1]})
        return users

    def verify_user(self, user_id, password):
        """
        Verifies if the provided user ID and password match an admin user.

        Args:
            user_id: The user ID to verify.
            password: The password to verify.

        Returns:
            True if the user is verified, False otherwise.

        """
        for user in self.users:
            if user['user_id'] == user_id and user['password'] == password:
                return True
        return False

    def admin_authority(self, app):
        """
        Displays the admin authority options and handles the selected option.

        Args:
            app: The FoodDeliveryApp instance.

        """
        print("***Admin login features***")
        print("1. Add new food items")
        print("2. Edit food items")
        print("3. View the list of all food items")
        print("4. Remove a food item from the menu")
        print("5. Go back")

        choice = input("Please enter your choice: ")

        if choice == "1":
            self.add_food_item(app)
        elif choice == "2":
            self.edit_food_item(app)
        elif choice == "3":
            self.view_food_items(app)
        elif choice == "4":
            self.remove_food_item(app)
        elif choice == "5":
            self.admin(app)
        else:
            print("Invalid choice. Please try again.")
            self.admin_authority(app)

    def add_food_item(self, app):
        """
        Adds a new food item to the menu.

        Args:
            app: The FoodDeliveryApp instance.

        """
        print("**Add new food item**")
        food_id = self.generate_food_id()

        name = input("Enter the name of the food item: ")
        quantity = input("Enter the quantity of the food item (For eg, 100ml, 250gm, 4pieces etc): ")
        price = input("Enter the price of the food item: ")
        discount = input("Enter the discount for the food item in %: ")
        stock = input("Enter the stock amount of the food item: ")

        food_item = {
            "FoodID": food_id,
            "Name": name,
            "Quantity": quantity,
            "Price": price,
            "Discount": discount,
            "Stock": stock
        }
        self.save_food_item(food_item)
        print("Food item added successfully!")
        print()
        self.admin_authority(app)

    def generate_food_id(self):
        """
        Generates a unique food ID for a new food item.

        Returns:
            A unique food ID.

        """
        with open(self.food_csv_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            existing_ids = {row[0] for row in reader}

        while True:
            food_id = random.randint(five_digit_low, five_digit_high)
            if str(food_id) not in existing_ids:
                break

        return food_id

    def save_food_item(self, food_item):
        """
        Saves a food item to the food CSV file.

        Args:
            food_item: The food item to save.

        """
        with open(self.food_csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                food_item['FoodID'],
                food_item['Name'],
                food_item['Quantity'],
                food_item['Price'],
                food_item['Discount'],
                food_item['Stock']
            ])

    def edit_food_item(self, app):
        """
        Edits an existing food item in the menu.

        Args:
            app: The FoodDeliveryApp instance.

        """
        print("**Edit food item**")
        food_id = input("Enter the FoodID of the food item to edit: ")

        if self.food_item_exists(food_id):
            existing_food_item = self.get_food_item(food_id)

            print("Existing details:")
            print()
            self.display_food_item(existing_food_item)
            print()

            updated_food_item = self.prompt_new_food_details(existing_food_item)

            self.update_food_item(updated_food_item)

            print("Food item updated successfully!")
        else:
            print("Food item does not exist.")
        print()
        self.admin_authority(app)

    def view_food_items(self, app):
        """
        Displays all food items in the menu.

        Args:
            app: The FoodDeliveryApp instance.

        """
        print("View all food items")
        with open(self.food_csv_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                food_item = self.row_to_food_item(row)
                self.display_food_item(food_item)
                print()
        self.admin_authority(app)

    def remove_food_item(self, app):
        """
        Removes a food item from the menu.

        Args:
            app: The FoodDeliveryApp instance.

        """
        print("Remove food item")
        food_id = input("Enter the FoodID of the food item to remove: ")

        if self.food_item_exists(food_id):
            self.delete_food_item(food_id)
            print("Food item removed successfully!")
        else:
            print("Food item does not exist.")
        print()
        self.admin_authority(app)

    def food_item_exists(self, food_id):
        """
        Checks if a food item with the given ID exists in the menu.

        Args:
            food_id: The FoodID to check.

        Returns:
            True if the food item exists, False otherwise.

        """
        with open(self.food_csv_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[0] == food_id:
                    return True
        return False

    def get_food_item(self, food_id):
        """
        Retrieves a food item from the menu using the given ID.

        Args:
            food_id: The FoodID of the food item to retrieve.

        Returns:
            The food item as a dictionary, or None if not found.

        """
        with open(self.food_csv_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[0] == food_id:
                    return self.row_to_food_item(row)
        return None

    def row_to_food_item(self, row):
        """
        Converts a CSV row to a food item dictionary.

        Args:
            row: The CSV row representing a food item.

        Returns:
            The food item as a dictionary.

        """
        return {
            "FoodID": row[0],
            "Name": row[1],
            "Quantity": row[2],
            "Price": row[3],
            "Discount": row[4],
            "Stock": row[5]
        }

    def display_food_item(self, food_item):
        """
        Displays the details of a food item.

        Args:
            food_item: The food item to display.

        """
        print(f"FoodID: {food_item['FoodID']}")
        print(f"Name: {food_item['Name']}")
        print(f"Quantity: {food_item['Quantity']}")
        print(f"Price: {food_item['Price']}")
        print(f"Discount: {food_item['Discount']}")
        print(f"Stock: {food_item['Stock']}")

    def prompt_new_food_details(self, existing_food_item):
        """
        Prompts the admin to enter new details for a food item.

        Args:
            existing_food_item: The existing food item.

        Returns:
            The updated food item as a dictionary.

        """
        print("Enter the new details (leave blank to keep existing):")
        new_name = input(f"Name ({existing_food_item['Name']}): ")
        new_quantity = input(f"Quantity ({existing_food_item['Quantity']}): ")
        new_price = input(f"Price ({existing_food_item['Price']}): ")
        new_discount = input(f"Discount ({existing_food_item['Discount']}): ")
        new_stock = input(f"Stock ({existing_food_item['Stock']}): ")

        updated_food_item = {
            "FoodID": existing_food_item["FoodID"],
            "Name": new_name if new_name else existing_food_item["Name"],
            "Quantity": new_quantity if new_quantity else existing_food_item["Quantity"],
            "Price": new_price if new_price else existing_food_item["Price"],
            "Discount": new_discount if new_discount else existing_food_item["Discount"],
            "Stock": new_stock if new_stock else existing_food_item["Stock"]
        }

        return updated_food_item

    def update_food_item(self, updated_food_item):
        """
        Updates an existing food item in the menu.

        Args:
            updated_food_item: The updated food item.

        """
        temp_csv_path = os.path.join(self.root, "temp_food.csv")
        with open(self.food_csv_path, 'r') as file, open(temp_csv_path, 'w', newline='') as temp_file:
            reader = csv.reader(file)
            writer = csv.writer(temp_file)
            writer.writerow(next(reader))
            for row in reader:
                if row[0] == updated_food_item["FoodID"]:
                    writer.writerow([
                        updated_food_item["FoodID"],
                        updated_food_item["Name"],
                        updated_food_item["Quantity"],
                        updated_food_item["Price"],
                        updated_food_item["Discount"],
                        updated_food_item["Stock"]
                    ])
                else:
                    writer.writerow(row)
        os.replace(temp_csv_path, self.food_csv_path)

    def delete_food_item(self, food_id):
        """
        Deletes a food item from the menu.

        Args:
            food_id: The FoodID of the food item to delete.

        """
        temp_csv_path = os.path.join(self.root, "temp_food.csv")
        with open(self.food_csv_path, 'r') as file, open(temp_csv_path, 'w', newline='') as temp_file:
            reader = csv.reader(file)
            writer = csv.writer(temp_file)
            writer.writerow(next(reader))
            for row in reader:
                if row[0] != food_id:
                    writer.writerow(row)
        os.replace(temp_csv_path, self.food_csv_path)


admin_functions = AdminFunctions()
