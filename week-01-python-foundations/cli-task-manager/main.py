# The previous code of rock, paper, scissors was a tutorial to get you started with Python. Now, we will build a simple command line task manager.The task manager will allow you to add tasks, view tasks, and mark tasks as complete.


Add_Task = "1. Add Task"
View_Tasks = "2. View Tasks"
Exit = "3. Exit"

tasks = ["dishes", "laundry", "vacuum"]

while True:
    print("Welcome to the Task Manager!")
    print(Add_Task)
    print(View_Tasks)
    print(Exit)

    choice = input("Enter your choice: ")

    if choice == "1":
        task = input("Enter a task: ")
        tasks.append(task)
        print(f"Task '{task}' added.")
    elif choice == "2":
        print("Tasks:")
        for i, task in enumerate(tasks):
            print(f"{i + 1}. {task}")
    elif choice == "3":
        print("Exiting Task Manager. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

        # Please try to solve this on your own first before reaching out on AI Challenge yourself mentally first.
        