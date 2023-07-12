class AgentApp:
    def __init__(self, database_file):
        self.database_file = database_file

    def display_customer_database(self):
        with open(self.database_file, "r") as file:
            for line in file:
                print(line.strip())

    def reset_customer_pin(self, account_number):
        with open(self.database_file, "r") as file:
            lines = file.readlines()

        found = False
        with open(self.database_file, "w") as file:
            for line in lines:
                row = line.strip().split(",")
                if row[2] == account_number:
                    row[3] = input("Enter a new 4-digit PIN: ")
                    found = True
                file.write(",".join(row) + "\n")

        if found:
            print("PIN reset successful.")
        else:
            print("Customer account not found.")

    def perform_customer_transaction(self, account_number):
        with open(self.database_file, "r") as file:
            lines = file.readlines()

        found = False
        with open(self.database_file, "w") as file:
            for line in lines:
                row = line.strip().split(",")
                if row[2] == account_number:
                    amount = float(input("Enter the transaction amount: "))
                    balance = float(row[4])
                    new_balance = balance + amount
                    row[4] = str(new_balance)
                    found = True
                file.write(",".join(row) + "\n")

        if found:
            print("Transaction completed.")
        else:
            print("Customer account not found.")

def main():
    print("Welcome to the Agent App")

    agent_app = AgentApp(database_file="database.txt")

    while True:
        print("\nMenu:")
        print("1. Display Customer Database")
        print("2. Reset Customer PIN")
        print("3. Perform Customer Transaction")
        print("4. Quit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            agent_app.display_customer_database()
        elif choice == "2":
            account_number = input("Enter customer's account number: ")
            agent_app.reset_customer_pin(account_number)
        elif choice == "3":
            account_number = input("Enter customer's account number: ")
            agent_app.perform_customer_transaction(account_number)
        elif choice == "4":
            print("Thank you for using the Agent App. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

