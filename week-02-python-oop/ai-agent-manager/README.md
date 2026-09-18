# Week 02 - Object-Oriented Programming (OOP)

## 90 Days of AI Agent Engineering

### Week 2 Focus

This week I focused on strengthening my understanding of **Object-Oriented Programming (OOP) in Python**.

After learning the concepts, I built a small **AI Agent Manager** to practise how classes, objects, inheritance, polymorphism and composition work together.

The goal wasn't to build a real AI agent connected to an LLM yet. The goal was to understand how Python OOP can be used to structure a system.

---

## What I Learned

This week I covered:

- Classes
- Objects
- `__init__`
- `self`
- Attributes
- Methods
- Encapsulation
- Inheritance
- Polymorphism
- Composition

---

# Project - AI Agent Manager

The AI Agent Manager is a Python OOP project where I can create different types of agents, give them tasks and control their status.

For example:

```python
agent1 = ResearchAgent("Research Agent", "Gemini")
agent2 = SupportAgent("Customer Support Agent", "GPT")
```

Each agent has its own:

- Name
- Model
- Status
- Tasks
- Behaviour

---

## Classes and Objects

I learned that a **class is a blueprint**, while an **object is an instance created from that blueprint**.

For example:

```python
class Agent:
    pass
```

`Agent` is the blueprint.

```python
agent1 = Agent("Research Agent", "Gemini")
```

`agent1` is an object created from that blueprint.

This helped me understand that I don't need to create a new class every time I want another agent.

---

## `__init__` and `self`

I used `__init__` to set up each Agent when it is created.

```python
def __init__(self, name, model, status="Offline"):
    self.name = name
    self.model = model
    self.status = status
    self.tasks = []
```

I learned that `self` refers to the **specific object currently using the class**.

This allows different Agent objects to have their own data.

For example:

```text
Research Agent
Model: Gemini
Status: Online

Customer Support Agent
Model: GPT
Status: Offline
```

---

## Methods

Methods define what an object can do.

My Agent objects can:

```text
introduce()
start()
stop()
add_task()
view_tasks()
perform_task()
```

For example:

```python
agent1.start()
```

changes the Research Agent's status to `Online`.

This helped me understand that objects can contain both **data and behaviour**.

---

## Inheritance

I created specialised agents that inherit from the main `Agent` class.

```python
class ResearchAgent(Agent):
    pass

class SupportAgent(Agent):
    pass
```

This means both agents can use functionality from `Agent` without rewriting everything.

I remember inheritance as:

> **"is a"**

A `ResearchAgent` **is an** `Agent`.

A `SupportAgent` **is an** `Agent`.

---

## Polymorphism

Both specialised agents have a `perform_task()` method, but they can perform it differently.

For example:

```text
Research Agent → researches information

Support Agent → helps a customer
```

This taught me that different objects can use the **same method name but have different behaviour**.

---

## Composition

I also created a separate `Task` class.

An Agent can contain multiple Task objects.

```text
Research Agent
│
├── Task
│   └── Research AI Agent frameworks
│
└── Task
    └── Compare Gemini and GPT models
```

This introduced me to **composition**.

I remember composition as:

> **"has a"**

An Agent **has Tasks**.

This is different from inheritance:

```text
ResearchAgent IS AN Agent → Inheritance

Agent HAS Tasks → Composition
```

---

## Encapsulation

Instead of changing an object's state everywhere in the program, I created methods that control those changes.

For example:

```python
agent1.start()
agent1.stop()
task1.complete()
```

The objects are responsible for updating their own state.

This gave me an introduction to the idea of encapsulation.

---

## How The Project Fits Together

```text
                    Agent
                   /     \
                  /       \
        ResearchAgent    SupportAgent
              |
              |
            Tasks
          /       \
       Task       Task
```

The project helped me understand how different objects can work together instead of putting all the logic into one large piece of code.

---

## Biggest Lessons From Week 2

One of my biggest lessons was understanding the difference between a **class and an object**.

At first, I thought I needed to create another class for every new Agent.

I now understand that I can create multiple objects from my classes:

```python
agent1 = ResearchAgent("Research Agent", "Gemini")
agent2 = SupportAgent("Customer Support Agent", "GPT")
```

I also have a much better understanding of why `self` and `__init__` are used and how inheritance and composition help organise Python applications.

---

## Why I'm Learning This

I currently work with AI Agent backend systems, so my goal isn't simply to memorise Python syntax.

I'm strengthening concepts I've already been exposed to so I can better understand how systems are structured, make better technical decisions, debug problems and explain the code I work with.

My learning process remains:

> **Learn → Build → Break → Debug → Understand → Document**

---
