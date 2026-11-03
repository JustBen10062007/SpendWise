from datetime import datetime
import re

# In-memory user data storage
users = {}


def validate_student_id(student_id):
    """Validates if student ID matches pattern '00-0000-000000' (2 digits - 4 digits - 6 digits)."""
    pattern = r"^\d{2}-\d{4}-\d{6}$"
    return bool(re.match(pattern, student_id))


def validate_full_name(name):
    """
    Validates that the name contains only letters, spaces, hyphens, or dots,
    and ensures it consists of at least two words (Full Name).
    """
    pattern = r"^[A-Za-z.-]+(?:\s+[A-Za-z.-]+)+$"
    return bool(re.match(pattern, name))


def register_user():
    print("\n--- USER REGISTRATION ---")

    while True:
        name = input(
            "Enter Full Name (e.g., Juan Dela Cruz or '0' to cancel): "
        ).strip()
        if name in ["0", "cancel"]:
            print("Registration cancelled.")
            return

        if not name:
            print("\n[ERROR] Full Name cannot be empty.")
            continue

        if not validate_full_name(name):
            print(
                "\n[INVALID FULL NAME] Please enter a valid full name (at least a First Name and Last Name). Numbers and special symbols are not allowed."
            )
            continue

        break

    while True:
        student_id = input(
            "Enter Student ID (Format: XX-XXXX-XXXXXX or '0' to cancel): "
        ).strip()
        if student_id in ["0", "cancel"]:
            print("Registration cancelled.")
            return

        if not validate_student_id(student_id):
            print(
                "\n[INVALID FORMAT] Student ID must follow the format '00-0000-000000' (e.g., 12-3456-789012)."
            )
            continue

        if student_id in users:
            print("\n[ERROR] A user with this Student ID is already registered.")
            return

        break

    password = input("Enter Password: ").strip()
    if not password:
        print("[ERROR] Password cannot be empty. Registration cancelled.")
        return

    users[student_id] = {
        "name": name,
        "password": password,
        "weekly_allowance": 0.0,
        "weekly_budget": 0.0,
        "expenses": [],
        "next_id": 1,
    }

    print(
        f"\nRegistration successful! Welcome, {name}. You can now log in using your Student ID."
    )


def login_user():
    print("\n--- USER LOGIN ---")
    if not users:
        print("No registered users found. Please register first.")
        return None

    student_id = input("Enter Student ID: ").strip()
    password = input("Enter Password: ").strip()

    if student_id in users and users[student_id]["password"] == password:
        print(f"\nLogin successful! Welcome back, {users[student_id]['name']}!")
        return users[student_id]
    else:
        print("\n[LOGIN FAILED] Invalid Student ID or Password.")
        return None


def get_float_input(prompt):
    """
    Helper function to get float input.
    Returns float value or None if user types '0' or 'cancel'.
    """
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() in ["cancel", "exit", "0"]:
            return None
        try:
            val = float(user_input)
            return val
        except ValueError:
            print("\nInvalid input! Enter a valid number or type '0' to cancel.")


def add_allowance(user):
    print("\n--- RECORD RECEIVED ALLOWANCE ---")
    print(f"Current Allowance Pool: ₱{user['weekly_allowance']:.2f}")

    amount = get_float_input("Enter allowance amount received (or '0' to cancel): ₱")
    if amount is None:
        print("Action cancelled. Returning to main menu...")
        return

    if amount <= 0:
        print("Allowance amount must be greater than zero.")
        return

    user["weekly_allowance"] += amount
    total_expenses = sum(item["amount"] for item in user["expenses"])
    remaining_balance = user["weekly_allowance"] - total_expenses

    print(f"\nSuccessfully added ₱{amount:.2f}!")
    print(f"Total Allowance Pool: ₱{user['weekly_allowance']:.2f}")
    print(f"Current Usable Balance: ₱{remaining_balance:.2f}")


def set_weekly_budget(user):
    print("\n--- SET WEEKLY BUDGET ---")

    amount = get_float_input("Enter Weekly Budget target (or '0' to cancel): ₱")
    if amount is None:
        print("Action cancelled. Returning to main menu...")
        return

    if amount <= 0:
        print("Weekly budget target must be greater than zero.")
        return

    user["weekly_budget"] = amount
    total_expenses = sum(item["amount"] for item in user["expenses"])
    budget_remaining = user["weekly_budget"] - total_expenses

    print(f"\nSuccessfully set Weekly Budget to ₱{user['weekly_budget']:.2f}!")

    if user["weekly_budget"] > user["weekly_allowance"]:
        difference = user["weekly_budget"] - user["weekly_allowance"]
        print(
            f"\n[WARNING] Your Weekly Budget (₱{user['weekly_budget']:.2f}) exceeds your Total Allowance Pool (₱{user['weekly_allowance']:.2f}) by ₱{difference:.2f}!"
        )
        print("You will need to add more allowance to spend up to this target.")

    if budget_remaining >= 0:
        print(f"Remaining Weekly Budget: ₱{budget_remaining:.2f}")
    else:
        print(
            f"Warning: You are already ₱{abs(budget_remaining):.2f} over this budget!"
        )


def create_expense(user):
    print("\n--- CREATE (Record Expense) ---")

    auto_date = datetime.now().strftime("%Y-%m-%d")

    print("\nSelect Category:")
    print("1. Food (e.g., Lunch, Snacks)")
    print("2. Transportation (e.g., Bus fare, Jeep, Taxi)")
    print("3. School Supplies (e.g., Books, Printing, Pens)")
    print("4. Others (Custom Category)")
    print("0. Return to Main Menu")

    cat_choice = input("Enter option (0-4): ").strip()
    if cat_choice in ["0", "cancel"]:
        print("Returning to main menu...")
        return

    categories = {
        "1": "Food",
        "2": "Transportation",
        "3": "School Supplies",
    }

    if cat_choice == "4":
        custom_cat = input("Enter custom category name (or '0' to cancel): ").strip()
        if custom_cat in ["0", "cancel"] or not custom_cat:
            print("Action cancelled.")
            return
        category = custom_cat.capitalize()
    elif cat_choice in categories:
        category = categories[cat_choice]
    else:
        print("Invalid category selected. Returning to main menu...")
        return

    description = input("Enter description (or '0' to cancel): ").strip()
    if description in ["0", "cancel"] or not description:
        print("Action cancelled.")
        return

    amount = get_float_input("Enter amount (or '0' to cancel): ₱")
    if amount is None:
        print("Action cancelled. Returning to main menu...")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    total_expenses = sum(item["amount"] for item in user["expenses"])
    remaining_balance = user["weekly_allowance"] - total_expenses

    if remaining_balance - amount < 0:
        print(
            "\nTransaction Declined! Adding this expense causes your balance to go below ₱0.00."
        )
        print(
            f"Current Usable Balance: ₱{remaining_balance:.2f} | Expense Attempted: ₱{amount:.2f}"
        )
        return

    if user["weekly_budget"] > 0 and (total_expenses + amount) > user["weekly_budget"]:
        print(
            f"\n[WARNING] This expense pushes total spent (₱{total_expenses + amount:.2f}) over your Weekly Budget (₱{user['weekly_budget']:.2f})!"
        )

    user["expenses"].append(
        {
            "id": user["next_id"],
            "date": auto_date,
            "category": category,
            "description": description,
            "amount": amount,
        }
    )

    print(
        f"Added '{description}' under [{category}] for ₱{amount:.2f} on {auto_date} (ID: {user['next_id']})"
    )
    user["next_id"] += 1


def display_expense_table(user):
    """Helper function to cleanly output the user's itemized expense table."""
    print(
        "\n---------------------------------------------------------------------------"
    )
    if not user["expenses"]:
        print("No expenses recorded yet.")
        print(
            "---------------------------------------------------------------------------"
        )
        return

    print(
        f"{'ID':<5} | {'Date':<10} | {'Category':<16} | {'Description':<20} | {'Amount':<10}"
    )
    print(
        "---------------------------------------------------------------------------"
    )

    for item in user["expenses"]:
        print(
            f"{item['id']:<5} | {item['date']:<10} | {item['category']:<16} | {item['description']:<20} | ₱{item['amount']:<10.2f}"
        )

    print(
        "---------------------------------------------------------------------------"
    )


def read_summary(user):
    print("\n==============================")
    print("     VIEW SPENDING SUMMARY    ")
    print("==============================")
    print("1. Daily Spending Summary")
    print("2. Weekly Spending Summary")
    print("3. Monthly Spending Summary")
    print("4. View All Expenses (Itemized)")
    print("0. Return to Main Menu")

    sub_choice = input("\nSelect view option (0-4): ").strip()
    if sub_choice in ["0", "cancel"]:
        print("Returning to main menu...")
        return

    total_expenses = sum(item["amount"] for item in user["expenses"])

    if sub_choice == "1":
        print("\n--- DAILY SPENDING SUMMARY ---")
        daily_totals = {}
        for item in user["expenses"]:
            date_str = item["date"]
            daily_totals[date_str] = daily_totals.get(date_str, 0.0) + item["amount"]

        if not daily_totals:
            print("No expenses recorded yet.")
        else:
            print(f"{'Date':<12} | {'Total Spent':<12}")
            print("----------------------------")
            for date_key, amount_sum in sorted(daily_totals.items()):
                print(f"{date_key:<12} | ₱{amount_sum:<12.2f}")

    elif sub_choice == "2":
        print("\n--- WEEKLY SPENDING SUMMARY ---")
        remaining = user["weekly_allowance"] - total_expenses
        budget_remaining = user["weekly_budget"] - total_expenses

        print(f"Total Weekly Allowance: ₱{user['weekly_allowance']:.2f}")
        if user["weekly_budget"] > 0:
            print(f"Weekly Budget Target:   ₱{user['weekly_budget']:.2f}")
        else:
            print("Weekly Budget Target:   Not set")

        print(f"Total Spent This Week:  ₱{total_expenses:.2f}")
        print(f"Usable Balance:         ₱{remaining:.2f}")

        if user["weekly_budget"] > 0:
            if budget_remaining >= 0:
                print(f"Weekly Budget Left:     ₱{budget_remaining:.2f}")
            else:
                print(
                    f"Weekly Budget Left:     -₱{abs(budget_remaining):.2f} (Over Budget!)"
                )

    elif sub_choice == "3":
        print("\n--- MONTHLY SPENDING SUMMARY ---")
        monthly_totals = {}
        for item in user["expenses"]:
            month_key = (
                item["date"][:7] if len(item["date"]) >= 7 else "Unknown"
            )
            monthly_totals[month_key] = (
                monthly_totals.get(month_key, 0.0) + item["amount"]
            )

        if not monthly_totals:
            print("No expenses recorded yet.")
        else:
            print(f"{'Month (YYYY-MM)':<16} | {'Total Spent':<12}")
            print("-----------------------------------")
            for m_key, amount_sum in sorted(monthly_totals.items()):
                print(f"{m_key:<16} | ₱{amount_sum:<12.2f}")

    elif sub_choice == "4":
        print("\n--- ALL ITEMIZED EXPENSES ---")
        display_expense_table(user)
    else:
        print("Invalid choice! Returning to main menu.")


def update_expense(user):
    print("\n--- UPDATE EXPENSE ---")
    if not user["expenses"]:
        print("No expenses recorded to update.")
        return

    print("\nCurrent Recorded Expenses:")
    display_expense_table(user)

    target_id_raw = get_float_input(
        "Enter Expense ID to update (or '0' to cancel): "
    )
    if target_id_raw is None:
        print("Action cancelled. Returning to main menu...")
        return

    target_id = int(target_id_raw)

    for item in user["expenses"]:
        if item["id"] == target_id:
            print(
                f"\nUpdating Expense #{target_id} (Leave blank to keep current value)"
            )

            new_date = input(f"Date [{item['date']}]: ").strip()
            if new_date:
                item["date"] = new_date

            new_desc = input(f"Description [{item['description']}]: ").strip()
            if new_desc:
                item["description"] = new_desc

            print("\nSelect New Category:")
            print("1. Food | 2. Transportation | 3. School Supplies | 4. Custom Category")
            cat_choice = input(f"Category [{item['category']}]: ").strip()
            categories = {
                "1": "Food",
                "2": "Transportation",
                "3": "School Supplies",
            }
            if cat_choice == "4":
                custom_cat = input("Enter custom category name: ").strip()
                if custom_cat:
                    item["category"] = custom_cat.capitalize()
            elif cat_choice in categories:
                item["category"] = categories[cat_choice]
            elif cat_choice != "":
                print("Invalid category selected. Keeping current category.")

            new_amount_str = input(
                f"Amount [₱{item['amount']:.2f}]: "
            ).strip()
            if new_amount_str:
                try:
                    new_val = float(new_amount_str)
                    if new_val <= 0:
                        print(
                            "Amount must be greater than zero. Keeping old value."
                        )
                    else:
                        other_expenses_total = sum(
                            i["amount"]
                            for i in user["expenses"]
                            if i["id"] != target_id
                        )
                        if (
                            user["weekly_allowance"]
                            - (other_expenses_total + new_val)
                            < 0
                        ):
                            print(
                                "Update Failed! This new amount causes your usable balance to go below ₱0.00."
                            )
                        else:
                            item["amount"] = new_val
                            print("Amount updated.")
                except ValueError:
                    print("Invalid input! Keeping old value.")

            print("Expense update process complete.")
            return

    print(f"Expense ID {target_id} not found.")


def delete_expense(user):
    print("\n--- DELETE EXPENSE ---")
    if not user["expenses"]:
        print("No expenses recorded to delete.")
        return

    print("\nCurrent Recorded Expenses:")
    display_expense_table(user)

    target_id_raw = get_float_input(
        "Enter Expense ID to delete (or '0' to cancel): "
    )
    if target_id_raw is None:
        print("Action cancelled. Returning to main menu...")
        return

    target_id = int(target_id_raw)

    for i in range(len(user["expenses"])):
        if user["expenses"][i]["id"] == target_id:
            removed = user["expenses"].pop(i)
            print(
                f"Deleted '{removed['description']}' (ID: {target_id}) successfully."
            )
            return

    print(f"Expense ID {target_id} not found.")


def spendwise_dashboard(current_user):
    """SpendWise main dashboard accessible only after logging in."""
    while True:
        print("\n==============================")
        print("          SPENDWISE           ")
        print("    Student Expense Tracker   ")
        print(f"    User: {current_user['name']}")
        print("==============================")
        print("1. Add Allowance")
        print("2. Set Weekly Budget (To Spend)")
        print("3. Add Expense (Create)")
        print("4. View Summary & Expenses (Read)")
        print("5. Update Expense (Update)")
        print("6. Delete Expense (Delete)")
        print("7. Log Out")

        choice = input("\nSelect an option (1-7): ").strip()

        if choice == "1":
            add_allowance(current_user)
        elif choice == "2":
            set_weekly_budget(current_user)
        elif choice == "3":
            create_expense(current_user)
        elif choice == "4":
            read_summary(current_user)
        elif choice == "5":
            update_expense(current_user)
        elif choice == "6":
            delete_expense(current_user)
        elif choice == "7":
            print(f"\nLogging out {current_user['name']}...")
            break
        else:
            print("Invalid choice. Please select between 1 and 7.")


def main():
    """System portal handling Login and Registration."""
    while True:
        print("\n==============================")
        print("   WELCOME TO SPENDWISE PORTAL")
        print("==============================")
        print("1. Register")
        print("2. Login")
        print("3. Exit System")

        choice = input("\nSelect an option (1-3): ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            logged_in_user = login_user()
            if logged_in_user:
                spendwise_dashboard(logged_in_user)
        elif choice == "3":
            print("\nThank you for using SpendWise Portal. Goodbye!")
            break
        else:
            print("Invalid choice. Please select between 1 and 3.")


if __name__ == "__main__":
    main()