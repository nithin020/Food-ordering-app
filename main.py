from utils.admin_functions import admin_functions
from utils.user_functions import user_functions


class FoodDeliveryApp:
    """
    A simple Food Delivery App that allows users to place orders and admins to manage the food items.
    """

    def __init__(self):
        """
        Initializes the FoodDeliveryApp class and starts the application.
        """
        self.run()

    def welcome_screen(self):
        """
        Displays the welcome screen of the app and prompts the user to choose an option.
        """
        print("Welcome to the Food Delivery App!")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Exit")

        choice = input("Please enter your choice: ")

        if choice == "1":
            self.admin_login()
        elif choice == "2":
            self.user_login()
        elif choice == "3":
            self.exit_program()
        else:
            print("Invalid choice. Please try again.")
            self.welcome_screen()

    def admin_login(self):
        """
        Prompts the admin to log in or register.
        """
        admin_functions.admin(self)

    def user_login(self):
        """
        Prompts the user to log in or register.
        """
        user_functions.user(self)

    def exit_program(self):
        """
        Exits the program.
        """
        print("Exiting the program. Goodbye!")

    def run(self):
        """
        Runs the Food Delivery App by displaying the welcome screen.
        """
        self.welcome_screen()


if __name__ == "__main__":
    app = FoodDeliveryApp()
