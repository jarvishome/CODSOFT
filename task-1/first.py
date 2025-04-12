import json
from datetime import datetime
import os

def main():
    tasks = load_tasks()
    
    while True:
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. View Tasks by Category")
        print("6. View Tasks by Priority")
        print("7. View Upcoming Tasks")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            mark_task_completed(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            view_by_category(tasks)
        elif choice == '6':
            view_by_priority(tasks)
        elif choice == '7':
            view_upcoming_tasks(tasks)
        elif choice == '8':
            save_tasks(tasks)
            print("\nTasks saved. Exiting the To-Do List Application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
            # Convert string dates back to datetime objects
            for task in tasks:
                if task['due_date']:
                    task['due_date'] = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    # Convert datetime objects to strings for JSON serialization
    tasks_to_save = []
    for task in tasks:
        task_copy = task.copy()
        if task_copy['due_date']:
            task_copy['due_date'] = task_copy['due_date'].strftime('%Y-%m-%d')
        else:
            task_copy['due_date'] = None
        tasks_to_save.append(task_copy)
    
    with open('tasks.json', 'w') as file:
        json.dump(tasks_to_save, file, indent=2)

def add_task(tasks):
    task = input("Enter the task: ")
    
    while True:
        category = input("Enter category (Work/Personal/Study/Other): ").capitalize()
        if category in ['Work', 'Personal', 'Study', 'Other']:
            break
        print("Please enter a valid category (Work/Personal/Study/Other)")
    
    while True:
        priority = input("Enter priority (High/Medium/Low): ").capitalize()
        if priority in ['High', 'Medium', 'Low']:
            break
        print("Please enter a valid priority (High/Medium/Low)")
    
    due_date = None
    while True:
        date_input = input("Enter due date (YYYY-MM-DD) or leave blank: ")
        if not date_input:
            break
        try:
            due_date = datetime.strptime(date_input, '%Y-%m-%d').date()
            if due_date < datetime.now().date():
                print("Due date cannot be in the past. Please enter a future date.")
                continue
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD or leave blank.")
    
    tasks.append({
        "task": task,
        "category": category,
        "priority": priority,
        "due_date": due_date,
        "completed": False,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    print(f"Task '{task}' added successfully!")

def view_tasks(tasks, task_list=None):
    if task_list is None:
        task_list = tasks
    
    if not task_list:
        print("No tasks found.")
        return
    
    print("\nTasks:")
    print(f"{'#':<3} | {'Status':<7} | {'Priority':<8} | {'Category':<8} | {'Due Date':<12} | Task")
    print("-" * 80)
    
    for index, task in enumerate(task_list, start=1):
        status = "✓" if task["completed"] else " "
        due_date = task["due_date"].strftime('%Y-%m-%d') if task["due_date"] else "No date"
        print(f"{index:<3} | [{status}] | {task['priority']:<8} | {task['category']:<8} | {due_date:<12} | {task['task']}")

def mark_task_completed(tasks):
    if not tasks:
        print("No tasks to mark as completed.")
        return
    
    view_tasks(tasks)
    try:
        task_num = int(input("Enter task number to mark as completed: "))
        if 1 <= task_num <= len(tasks):
            tasks[task_num-1]["completed"] = True
            print(f"Task '{tasks[task_num-1]['task']}' marked as completed!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def delete_task(tasks):
    if not tasks:
        print("No tasks to delete.")
        return
    
    view_tasks(tasks)
    try:
        task_num = int(input("Enter task number to delete: "))
        if 1 <= task_num <= len(tasks):
            deleted_task = tasks.pop(task_num-1)
            print(f"Task '{deleted_task['task']}' deleted successfully!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def view_by_category(tasks):
    categories = sorted(set(task['category'] for task in tasks))
    if not categories:
        print("No categories found.")
        return
    
    print("\nAvailable categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    
    try:
        choice = int(input("Select category number: "))
        if 1 <= choice <= len(categories):
            selected_category = categories[choice-1]
            filtered_tasks = [task for task in tasks if task['category'] == selected_category]
            print(f"\nTasks in category '{selected_category}':")
            view_tasks(tasks, filtered_tasks)
        else:
            print("Invalid category number.")
    except ValueError:
        print("Please enter a valid number.")

def view_by_priority(tasks):
    priorities = ['High', 'Medium', 'Low']
    print("\nAvailable priorities:")
    for i, priority in enumerate(priorities, 1):
        print(f"{i}. {priority}")
    
    try:
        choice = int(input("Select priority number: "))
        if 1 <= choice <= len(priorities):
            selected_priority = priorities[choice-1]
            filtered_tasks = [task for task in tasks if task['priority'] == selected_priority]
            print(f"\nTasks with priority '{selected_priority}':")
            view_tasks(tasks, filtered_tasks)
        else:
            print("Invalid priority number.")
    except ValueError:
        print("Please enter a valid number.")

def view_upcoming_tasks(tasks):
    today = datetime.now().date()
    upcoming_tasks = []
    
    for task in tasks:
        if task['due_date'] and not task['completed']:
            days_remaining = (task['due_date'] - today).days
            if days_remaining >= 0:
                task_with_days = task.copy()
                task_with_days['days_remaining'] = days_remaining
                upcoming_tasks.append(task_with_days)
    
    if not upcoming_tasks:
        print("No upcoming tasks with due dates.")
        return
    
    # Sort by days remaining (ascending)
    upcoming_tasks.sort(key=lambda x: x['days_remaining'])
    
    print("\nUpcoming Tasks:")
    print(f"{'#':<3} | {'Priority':<8} | {'Category':<8} | {'Due In':<8} | {'Due Date':<12} | Task")
    print("-" * 80)
    
    for index, task in enumerate(upcoming_tasks, start=1):
        due_in = f"{task['days_remaining']} days" if task['days_remaining'] > 0 else "Today"
        print(f"{index:<3} | {task['priority']:<8} | {task['category']:<8} | {due_in:<8} | {task['due_date'].strftime('%Y-%m-%d'):<12} | {task['task']}")

if __name__ == "__main__":
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
