import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class ToDoList:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated To-Do List")
        self.tasks = []

        self.task_label = tk.Label(root, text="Task:")
        self.task_label.pack()

        self.task_entry = tk.Entry(root, width=30)
        self.task_entry.pack()

        self.date_label = tk.Label(root, text="Due Date (MM-DD-YYYY):")
        self.date_label.pack()

        self.date_entry = tk.Entry(root, width=30)
        self.date_entry.pack()

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.sort_button = tk.Button(root, text="Sort", command=self.sort_tasks)
        self.sort_button.pack()

        self.task_listbox = tk.Listbox(root, width=50)
        self.task_listbox.pack()

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

        self.overdue_button = tk.Button(root, text="Check for Overdue Tasks", command=self.check_overdue)
        self.overdue_button.pack()

        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get().strip()
        date = self.date_entry.get().strip()
        if task and date:
            try:
                task_date = datetime.strptime(date, "%m-%d-%Y")
                task_entry = (task, date)
                self.tasks.append(task_entry)
                self.task_listbox.insert(tk.END, f"{task} - Due: {date}")
                self.task_entry.delete(0, tk.END)
                self.date_entry.delete(0, tk.END)
                self.save_tasks()
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter a valid date in the format MM-DD-YYYY.")
        else:
            messagebox.showerror("Missing Information", "Please enter both the task and the due date.")
        self.sort_tasks()

    def sort_tasks(self):
        self.tasks.sort(key=lambda task: datetime.strptime(task[1], "%m-%d-%Y"))
        self.task_listbox.delete(0, tk.END)
        for task, date in self.tasks:
            self.task_listbox.insert(tk.END, f"{task} - Due: {date}")
        self.save_tasks()
        self.check_overdue()

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            task, date = self.tasks[index]
            confirm_delete = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete the task '{task}' due on {date}?",
            )
            if confirm_delete:
                del self.tasks[index]
                self.task_listbox.delete(index)
                self.save_tasks()
        else:
            messagebox.showerror("No Task Selected", "Please select a task to delete.")
        self.sort_tasks()

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task, date in self.tasks:
                file.write(f"{task},{date}\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                for line in file:
                    task, date = line.strip().split(',')
                    self.tasks.append((task, date))
                    self.task_listbox.insert(tk.END, f"{task} - Due: {date}")
        except FileNotFoundError:
            pass
        self.sort_tasks()
        self.check_overdue()

    def check_overdue(self):
        for task, date in self.tasks:
            if datetime.strptime(date, "%m-%d-%Y") < datetime.now():
                messagebox.showerror("Overdue Task", f"The task '{task}' is overdue.")
            else:
                pass


if __name__ == "__main__":
    root = tk.Tk()
    todo_list = ToDoList(root)
    root.mainloop()
