import json
import csv
import os
import datetime
from pathlib import Path

# --- MODULE 1: DATA MODELS ---
class Expense:
    def __init__(self, date, amount, category, description):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

    def to_dict(self):
        return {
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }

# --- MODULE 2: FILE HANDLING ---
class FileHandler:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)

    def save(self, data):
        try:
            with open(self.filename, 'w') as f:
                json.dump([e.to_dict() for e in data], f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    def load(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                raw_data = json.load(f)
                return [Expense(**item) for item in raw_data]
        except (json.JSONDecodeError, KeyError):
            print("Warning: Data file corrupted. Starting fresh.")
            return []

    def export_csv(self, data):
        filename = f"report_{datetime.date.today()}.csv"
        keys = ["date", "amount", "category", "description"]
        with open(filename, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows([e.to_dict() for e in data])
        return filename

    def create_backup(self):
        if os.path.exists(self.filename):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"backup_{timestamp}.json"
            import shutil
            shutil.copy(self.filename, backup_path)
            return backup_path
        return None

# --- MODULE 3: REPORTING & LOGIC ---
class FinanceTracker:
    def __init__(self):
        self.file_handler = FileHandler()
        self.expenses = self.file_handler.load()
        self.budget = 0.0

    def add_expense(self, date, amount, category, desc):
        new_expense = Expense(date, amount, category, desc)
        self.expenses.append(new_expense)
        self.file_handler.save(self.expenses)

    def get_monthly_total(self, month, year):
        return sum(e.amount for e in self.expenses 
                   if e.date.startswith(f"{year}-{month:02}"))

    def get_category_breakdown(self):
        breakdown = {}
        for e in self.expenses:
            breakdown[e.category] = breakdown.get(e.category, 0) + e.amount
        return breakdown

# --- MODULE 4: USER INTERFACE ---
class AppUI:
    def __init__(self):
        self.tracker = FinanceTracker()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_valid_float(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a number.")

    def run(self):
        while True:
            print("\n" + "="*30)
            print(" PERSONAL FINANCE TRACKER ")
            print("="*30)
            print("1. Add Expense")
            print("2. View All")
            print("3. Monthly Report")
            print("4. Category Breakdown (Visual)")
            print("5. Export CSV")
            print("6. Backup Data")
            print("0. Exit")
            
            choice = input("\nChoice: ")

            if choice == '1':
                date = input("Date (YYYY-MM-DD) [Empty for today]: ") or str(datetime.date.today())
                amt = self.get_valid_float("Amount: ")
                cat = input("Category (Food, Rent, Fun, etc): ").capitalize()
                desc = input("Description: ")
                self.tracker.add_expense(date, amt, cat, desc)
                print("Added!")

            elif choice == '2':
                print(f"\n{'Date':<12} | {'Category':<10} | {'Amount':<8} | {'Description'}")
                print("-" * 50)
                for e in self.tracker.expenses:
                    print(f"{e.date:<12} | {e.category:<10} | ${e.amount:<7.2f} | {e.description}")

            elif choice == '3':
                m = int(input("Month (1-12): "))
                y = int(input("Year (YYYY): "))
                total = self.tracker.get_monthly_total(m, y)
                print(f"\nTotal Spending for {m}/{y}: ${total:.2f}")

            elif choice == '4':
                data = self.tracker.get_category_breakdown()
                if not data: continue
                max_val = max(data.values())
                print("\n--- Category Breakdown ---")
                for cat, amt in data.items():
                    bar = "█" * int((amt/max_val) * 20)
                    print(f"{cat:<10} | {bar} ${amt:.2f}")

            elif choice == '5':
                fname = self.tracker.file_handler.export_csv(self.tracker.expenses)
                print(f"Exported to {fname}")

            elif choice == '6':
                path = self.tracker.file_handler.create_backup()
                print(f"Backup created at: {path}" if path else "No data to backup.")

            elif choice == '0':
                print("Goodbye!")
                break

if __name__ == "__main__":
    app = AppUI()
    app.run()
