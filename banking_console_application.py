class BankAccount:
    """Represents a bank account and manages its transactions."""

    def __init__(self, opening_balance: float = 10000.0):
        if opening_balance < 0:
            raise ValueError("Opening balance cannot be negative.")

        self._balance = opening_balance

    def check_balance(self) -> float:
        """Return the current account balance."""
        return self._balance

    def deposit(self, amount: float) -> bool:
        """Deposit money if the amount is valid."""

        if amount <= 0:
            print("Error: Deposit amount must be greater than zero.")
            return False

        self._balance += amount

        print("Deposit successful.")
        print(f"Updated Balance: ₹{self._balance:.2f}")

        return True

    def withdraw(self, amount: float) -> bool:
        """Withdraw money if the amount is valid and funds are sufficient."""

        if amount <= 0:
            print("Error: Withdrawal amount must be greater than zero.")
            return False

        if amount > self._balance:
            print("Transaction failed: Insufficient balance.")
            print(f"Current Balance: ₹{self._balance:.2f}")
            return False

        self._balance -= amount

        print("Withdrawal successful.")
        print(f"Updated Balance: ₹{self._balance:.2f}")

        return True


class BankingApp:
    """Handles the console interface for the banking application."""

    def __init__(self):
        self.account = BankAccount()
    
    def display_menu(self) -> None:
        """Display the banking menu."""

        print("\n1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Exit")

    @staticmethod
    def get_amount(prompt: str) -> float | None:
        """Read a numeric transaction amount."""

        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Please enter a valid numeric amount.")
            return None

    def run(self) -> None:
        """Run the application until the user exits."""

        print("Welcome to Kiran Bank")
        print(f"Opening Balance: ₹{self.account.check_balance():.2f}")

        while True:
            self.display_menu()

            choice = input("Enter choice: ").strip()

            if choice == "1":
                balance = self.account.check_balance()
                print(f"Current Balance: ₹{balance:.2f}")

            elif choice == "2":
                amount = self.get_amount("Enter deposit amount: ")

                if amount is not None:
                    self.account.deposit(amount)

            elif choice == "3":
                amount = self.get_amount("Enter withdrawal amount: ")

                if amount is not None:
                    self.account.withdraw(amount)

            elif choice == "4":
                print("Thank you for banking with us. Goodbye!")
                break

            else:
                print("Invalid choice. Please select an option from 1 to 4.")


if __name__ == "__main__":
    app = BankingApp()
    app.run()