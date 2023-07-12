import random

class BankApp:
    def __init__(self, database_file):
        self.users = []
        self.database_file = database_file

    def create_account(self):
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")

        # Check if the first and last name combination already exists
        if self.is_duplicate_name(first_name, last_name):
            print("An account with the same first and last name combination already exists.")
            return
        
        while True:
            pin = input("Enter a 4-digit PIN: ")
            if len(pin) != 4 or not pin.isdigit():
                print("Invalid PIN. PIN must be a 4-digit number.")
            else:
                break
        account_number = self.generate_account_number()

        user = {
            "First Name": first_name,
            "Last Name": last_name,
            "Account Number": account_number,
            "PIN": pin,
            "Balance": 0.0,
            "PIN Attempts": 0
        }

        self.users.append(user)
        self.save_data()

        print("Account created successfully.")
        print(f"Account Number: {account_number}")
        print(f"PIN: {pin}")

    def generate_account_number(self):
        while True:
            # Generate a random 10-digit account number
            account_number = random.randint(1000000000, 9999999999)

            # Check if the account number already exists in the users' list
            if not any(user["Account Number"] == account_number for user in self.users):
                return account_number

    def save_data(self):
        with open(self.database_file, "w") as file:
            for user in self.users:
                for key, value in user.items():
                    line = f"{key}: {value}\n"
                    file.write(line)
                file.write("\n")

    def load_data(self):
        try:
            with open(self.database_file, "r") as file:
                lines = file.readlines()
                user = {}
                for line in lines:
                    line = line.strip()
                    if line:
                        if ":" in line:
                            key, value = line.split(":", 1)
                            user[key.strip()] = value.strip()
                    else:
                        self.users.append(user)
                        user = {}
        except FileNotFoundError:
            pass

    def is_duplicate_name(self, first_name, last_name):
        for user in self.users:
            if user["First Name"] == first_name and user["Last Name"] == last_name:
                return True
        return False
    
    def authenticate(self, account_number, pin):
        # Check if the provided account number and pin are valid
        for user in self.users:
            if str(user["Account Number"]) == str(account_number) and str(user["PIN"]) == str(pin):
                return user
        return None

    def get_user_by_account_number(self, account_number):
        # Convert the account number to an integer
        account_number = int(account_number)

        # Retrieve the user's details from the users' list
        for user in self.users:
            if int(user["Account Number"]) == account_number:
                return user
        return None

    def check_balance(self, user):
        print("Account Details:")
        print(f"First Name: {user['First Name']}")
        print(f"Last Name: {user['Last Name']}")
        print(f"Account Number: {user['Account Number']}")
        print(f"PIN: {user['PIN']}")
        print(f"Balance: ${user['Balance']}")

    def transfer(self, sender):
        recipient_account_number = input("Enter the recipient's account number: ")
        recipient = self.get_user_by_account_number(recipient_account_number)
        if not recipient:
            print("Recipient account not found.")
            return

        print(f"Transfer to: {recipient['First Name']} {recipient['Last Name']}")
        confirm = input("Confirm recipient? (yes/no): ")

        if confirm.lower() == "yes":
            amount = float(input("Enter the amount to transfer: "))

            pin_attempts = 0
            while pin_attempts < 3:
                pin = input("Enter your 4-digit PIN to confirm: ")
                if pin != sender["PIN"]:
                    pin_attempts += 1
                    print(f"Incorrect PIN. {3 - pin_attempts} more attempts.")
                else:
                    break

            if pin_attempts == 3:
                print("Account locked. Contact customer service for assistance.")
            elif amount > sender["Balance"]:
                print("Insufficient balance.")
            else:
                # Update the sender's balance
                sender["Balance"] -= amount

                # Update the recipient's balance
                recipient["Balance"] += amount

                print("Transfer successful.")
        elif confirm.lower() == "no":
            print("Transfer canceled.")
        else:
            print("Invalid input. Transfer canceled.")

    def reset_pin(self, user):
        account_number = str(user["Account Number"])
        hidden_account_number = account_number[:3] + "xxxx" + account_number[7:]
        confirmation_account_number = account_number[:3] + "xxxx" + account_number[7:10]
        
        print(f"Please enter the following digits of your account number: {confirmation_account_number}")

        while True:
            confirmation_digits = input("Please enter the digits: ")
            if confirmation_digits != account_number[3:7]:
                print("Invalid digits. Please enter the correct digits of your account number.")
            else:
                break

        new_pin = input("Enter a new 4-digit PIN: ")
        if len(new_pin) != 4 or not new_pin.isdigit():
            print("Invalid PIN. PIN must be a 4-digit number.")
            return

        user["PIN"] = new_pin

        print("PIN reset successful.")

def main():
    print("Welcome to Chuka's bank app")

    customer_app = BankApp(database_file="database.txt")
    customer_app.load_data()

    while True:
        print("\nMenu:")
        print("1. Create a new account")
        print("2. Login")
        print("3. Quit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            customer_app.create_account()
        elif choice == "2":
            while True:
                account_number = input("Enter your account number: ")
                pin = input("Enter your 4-digit PIN: ")
                user = customer_app.authenticate(account_number, pin)
                if user:
                    print(f"Welcome, {user['First Name']} {user['Last Name']}!")
                    logged_in = True
                    while logged_in:
                        print("\nAccount Menu:")
                        print("1. Check Account Details")
                        print("2. Check Balance")
                        print("3. Transfer Money")
                        print("4. Reset PIN")
                        print("5. Logout")

                        account_choice = input("Enter your choice (1-5): ")

                        if account_choice == "1":
                            customer_app.check_balance(user)
                        elif account_choice == "2":
                            print(f"Balance: ${user['Balance']}")
                        elif account_choice == "3":
                            customer_app.transfer(user)
                        elif account_choice == "4":
                            customer_app.reset_pin(user)
                        elif account_choice == "5":
                            logged_in = False
                        else:
                            print("Invalid choice. Please try again.")
                    break
                else:
                    print("Invalid account number or PIN. Please try again.")
        elif choice == "3":
            print("Thank you for using our bank app. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    
