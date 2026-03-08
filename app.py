import tkinter as tk
from speech_engine import get_voice_input
from database import init_db, add_task, get_tasks, delete_task, mark_task_done, get_completed_tasks, get_full_table

# ---- refresh main list with numbering ----
def refresh_list():
    listbox.delete(0, tk.END)
    global current_tasks
    current_tasks = []
    tasks = get_tasks()
    for i, (tid, task, done) in enumerate(tasks, start=1):
        label = f"{i}. {'✓ ' if done == 1 else ''}{task}"
        listbox.insert(tk.END, label)
        current_tasks.append(tid)

# ---- add manually ----
def handle_manual_add():
    task = entry.get()
    if task:
        add_task(task)
        entry.delete(0, tk.END)
        refresh_list()

# ---- add using live voice ----
def handle_voice_add():
    listening_label = tk.Label(root, text="🎙 Listening…", fg="blue")
    listening_label.pack()
    root.update()

    task = get_voice_input()
    listening_label.destroy()

    if task:
        add_task(task)
        refresh_list()

# ---- mark as done ----
def handle_mark_done():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        tid = current_tasks[index]
        mark_task_done(tid)
        refresh_list()

# ---- delete ----
def handle_delete():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        tid = current_tasks[index]
        delete_task(tid)
        refresh_list()

# ---- refresh completed list ----
def refresh_completed_listbox(completed_listbox):
    completed_listbox.delete(0, tk.END)
    completed_tasks = get_completed_tasks()
    if not completed_tasks:
        completed_listbox.insert(tk.END, "No completed tasks yet.")
    else:
        for i, (tid, task) in enumerate(completed_tasks, start=1):
            completed_listbox.insert(tk.END, f"{i}. {task}")

# ---- show completed ----
def show_completed_tasks():
    completed_window = tk.Toplevel(root)
    completed_window.title("✅ Completed Tasks")
    completed_window.geometry("300x300")

    completed_listbox = tk.Listbox(completed_window, width=40, height=12)
    completed_listbox.pack(pady=10)

    tk.Button(
        completed_window,
        text="🔄 Refresh",
        command=lambda: refresh_completed_listbox(completed_listbox)
    ).pack(pady=5)

    refresh_completed_listbox(completed_listbox)

# ---- show full database table ----
from tkinter import ttk
from database import get_full_table

def show_full_table():
    db_window = tk.Toplevel(root)
    db_window.title("🗃 Database Table")
    db_window.geometry("500x300")

    # Create a Treeview (table)
    columns = ("ID", "Task", "Done")
    tree = ttk.Treeview(db_window, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Task", text="Task")
    tree.heading("Done", text="Done")
    tree.column("ID", width=50, anchor="center")
    tree.column("Task", width=300, anchor="w")
    tree.column("Done", width=80, anchor="center")
    tree.pack(fill="both", expand=True)

    # Insert data into the table
    data = get_full_table()
    if not data:
        tree.insert("", "end", values=("No data", "", ""))
    else:
        for row in data:
            done_status = "✅" if row[2] == 1 else "❌"
            tree.insert("", "end", values=(row[0], row[1], done_status))

# ---- GUI setup ----
root = tk.Tk()
root.title("🎙 Voice To-Do List")
root.geometry("400x500")

init_db()

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

tk.Button(root, text="➕ Add Task", command=handle_manual_add).pack()
tk.Button(root, text="🎤 Voice Add", command=handle_voice_add).pack()
tk.Button(root, text="✔ Mark as Done", command=handle_mark_done).pack()
tk.Button(root, text="🗑 Delete Task", command=handle_delete).pack()
tk.Button(root, text="📋 View Completed", command=show_completed_tasks).pack()
tk.Button(root, text="🗃 View Database Table", command=show_full_table).pack()  # 👈 NEW BUTTON

listbox = tk.Listbox(root, width=40, height=12)
listbox.pack(pady=10)

refresh_list()
root.mainloop()
