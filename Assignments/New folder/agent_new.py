class AgentApp:
    def __init__(self, database_file):
        self.database_file = database_file
        self.users = []  # List to hold customer data

    def load_data(self):
        try:
            with open(self.database_file, "r") as file:
                lines = file.readlines()
                user = {}
                for line in lines:
                    line = line.strip()
                    if line:
                        key, value = line.split(":")
                        user[key.strip()] = value.strip()
                    else:
                        self.users.append(user)
                        user = {}
        except FileNotFoundError:
            pass

    def display_customer_database(self):
        self.load_data()
        for user in self.users:
            print("Customer Details:")
            print(f"First Name: {user['first_name']}")
            print(f"Last Name: {user['last_name']}")
            print(f"Account Number: {user['account_number']}")
            print(f"PIN: {user['pin']}")
            print(f"Balance: {user['balance']}")
            print()

    def reset_customer_pin(self, account_number):
        self.load_data()
        found = False

        for user in self.users:
            if user["account_number"] == account_number:
                found = True
                break

        if found:
            print(f"Account found for: {user['first_name']} {user['last_name']}")
            confirm = input("Are you sure you want to reset the PIN? (yes/no): ")
            if confirm.lower() == "yes":
                new_pin = input("Enter a new 4-digit PIN: ")
                user["pin"] = new_pin
                self.save_data()
                print("PIN reset successful.")
            else:
                print("PIN reset cancelled.")
        else:
            print("Customer account not found.")

    def perform_customer_transaction(self, account_number):
        self.load_data()
        found_sender = False
        found_recipient = False
        sender = None
        recipient = None

        for user in self.users:
            if user["account_number"] == account_number:
                sender = user
                found_sender = True
                break

        if found_sender:
            recipient_account_number = input("Enter recipient's account number: ")
            for user in self.users:
                if user["account_number"] == recipient_account_number:
                    recipient = user
                    found_recipient = True
                    break

        if found_sender and found_recipient:
            print(f"Sender: {sender['first_name']} {sender['last_name']}")
            confirm_sender = input("Confirm sender? (yes/no): ")
            if confirm_sender.lower() == "yes":
                print(f"Recipient: {recipient['first_name']} {recipient['last_name']}")
                confirm_recipient = input("Confirm recipient? (yes/no): ")
                if confirm_recipient.lower() == "yes":
                    amount = float(input("Enter the amount to transfer: "))

                    sender_balance = float(sender["balance"])
                    recipient_balance = float(recipient["balance"])

                    if amount > sender_balance:
                        print("Insufficient balance.")
                        print("Transaction cancelled.")
                    else:
                        # Update the sender's balance
                        sender_balance -= amount
                        sender["balance"] = str(sender_balance)

                        # Update the recipient's balance
                        recipient_balance += amount
                        recipient["balance"] = str(recipient_balance)

                        self.save_data()
                        print("Transaction completed.")
                else:
                    print("Transaction cancelled.")
            else:
                print("Transaction cancelled.")
        else:
            print("Sender or recipient account not found.")

    def save_data(self):
        with open(self.database_file, "w") as file:
            for user in self.users:
                for key, value in user.items():
                    line = f"{key}: {value}\n"
                    file.write(line)
                file.write("\n")

    def main(self):
        print("Welcome to the Agent App")

        while True:
            print("\nMenu:")
            print("1. Display Customer Database")
            print("2. Reset Customer PIN")
            print("3. Perform Customer Transaction")
            print("4. Quit")

            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                self.display_customer_database()
            elif choice == "2":
                account_number = input("Enter customer's account number: ")
                self.reset_customer_pin(account_number)
            elif choice == "3":
                account_number = input("Enter customer's account number: ")
                self.perform_customer_transaction(account_number)
            elif choice == "4":
                print("Thank you for using the Agent App. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    agent_app = AgentApp(database_file="database.txt")
    agent_app.main()
