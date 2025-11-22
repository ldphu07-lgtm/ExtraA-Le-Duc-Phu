from gradebook import GradebookManager


def print_table(courses):
    print("-" * 85)
    print(f"{'Code':<10} | {'Name':<25} | {'Credits':<8} | {'Semester':<15} | {'Score':<5}")
    print("-" * 85)
    for c in courses:
        print(
            f"{c['code']:<10} | {c['name']:<25} | {c['credits']:<8} | {c['semester']:<15} | {c['score']:<5}")
    print("-" * 85)


def get_valid_number(prompt, data_type=float, max_value=None):
    while True:
        try:
            value = data_type(input(prompt))

            if value < 0:
                print("A positive number is required")
                continue

            if max_value is not None and value > max_value:
                print(f"please enter (0-{max_value})")
                continue
            return value

        except ValueError:
            print(
                f"Error: Please enter a valid number ({data_type.__name__}).")


def main():
    manager = GradebookManager()

    while True:
        print("\n=== STUDENT GRADEBOOK CLI - Le Duc Phu ===")
        print("1. Add a Course")
        print("2. Update a Course")
        print("3. Delete a Course")
        print("4. View Gradebook")
        print("5. Calculate GPA")
        print("6. Exit")

        choice = input("Select an option (1-6): ")

        if choice == '1':
            code = input("Enter Course Code: ").strip()
            if not code:
                print("Error: Code cannot be empty.")
                continue
            name = input("Enter Course Name: ")

            credits = get_valid_number("Enter Credits (int): ", int)

            semester = input("Enter Semester (e.g., Summer2025): ")

            score = get_valid_number("Enter Score (0-4): ", float, max_value=4)

            success, message = manager.add_course(
                code, name, credits, semester, score)
            print(f">> {message}")

        elif choice == '2':
            code = input("Enter Course Code to Update: ")
            print("Search for Course...")

            new_score = get_valid_number(
                "Enter New Score (0-4): ", float, max_value=4)

            if manager.update_course(code, {'score': new_score}):
                print(">> Update successful.")
            else:
                print(">> Course not found.")

        elif choice == '3':
            code = input("Enter Course Code to Delete: ")
            if manager.delete_course(code):
                print(">> Deleted successfully.")
            else:
                print(">> Course not found.")

        elif choice == '4':
            courses = manager.get_all_courses()
            if not courses:
                print(">> No courses found.")
            else:
                print_table(courses)

        elif choice == '5':
            print("a. Overall GPA")
            print("b. GPA by Semester")
            sub = input("Choose (a/b): ").lower()
            if sub == 'a':
                gpa = manager.calculate_gpa()
                print(f">> Overall Weighted GPA: {gpa}")
            elif sub == 'b':
                sem = input("Enter Semester name: ")
                gpa = manager.calculate_gpa(semester=sem)
                print(f">> GPA for {sem}: {gpa}")

        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
