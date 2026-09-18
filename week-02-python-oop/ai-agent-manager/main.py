# Week 02 - Object-Oriented Programming
# Project: AI Agent Manager
#
# Concepts:
# - Classes and Objects
# - __init__
# - self
# - Attributes
# - Methods
# - Encapsulation
# - Inheritance
# - Polymorphism
# - Composition



# COMPOSITION


class Task:

    def __init__(self, title):
        self.title = title
        self.completed = False

    def complete(self):
        self.completed = True

    def display(self):
        status = "Completed" if self.completed else "Pending"
        print(f"{self.title} - {status}")



# PARENT CLASS


class Agent:

    def __init__(self, name, model, status="Offline"):
        self.name = name
        self.model = model
        self.status = status
        self.tasks = []

    def introduce(self):
        print(
            f"Hello, I am {self.name}, "
            f"a {self.model} model. "
            f"My current status is {self.status}."
        )

    def start(self):
        self.status = "Online"
        print(f"{self.name} is now Online.")

    def stop(self):
        self.status = "Offline"
        print(f"{self.name} is now Offline.")

    def add_task(self, task):
        self.tasks.append(task)
        print(f"Task '{task.title}' added to {self.name}.")

    def view_tasks(self):
        print(f"\nTasks for {self.name}:")

        if not self.tasks:
            print("No tasks assigned.")
            return

        for task in self.tasks:
            task.display()

    def perform_task(self):
        print(f"{self.name} is performing a general task.")



# INHERITANCE


class ResearchAgent(Agent):

    def perform_task(self):
        print(f"{self.name} is researching information.")


class SupportAgent(Agent):

    def perform_task(self):
        print(f"{self.name} is helping a customer.")


# CREATE OBJECTS


agent1 = ResearchAgent(
    "Research Agent",
    "Gemini"
)

agent2 = SupportAgent(
    "Customer Support Agent",
    "GPT"
)



# USE THE OBJECTS


agent1.introduce()
agent2.introduce()

agent1.start()

print()

agent1.perform_task()
agent2.perform_task()


# CREATE TASK OBJECTS


task1 = Task("Research AI Agent frameworks")
task2 = Task("Compare Gemini and GPT models")



# GIVE TASKS TO AN AGENT

agent1.add_task(task1)
agent1.add_task(task2)

agent1.view_tasks()



# COMPLETE A TASK


task1.complete()

agent1.view_tasks()

agent1.stop()