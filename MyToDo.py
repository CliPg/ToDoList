import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk, font
import json
import os
from datetime import datetime
from PIL import Image, ImageDraw
import pystray
import threading

# 初始化 CustomTkinter 应用
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# 使用绝对路径保存文件
DATA_FILE = os.path.join(os.path.expanduser("~"), "todo_data.json")

# 全部任务数据
all_tasks = []

# 添加任务
def add_task():
    task = entry_task.get()
    deadline = date_entry.get_date().strftime('%Y-%m-%d')
    status = status_var.get()
    if task and deadline:
        tree.insert("", "end", values=(task, deadline, status))
        entry_task.delete(0, "end")
        date_entry.set_date(datetime.today())
        status_var.set("Pending")
        save_tasks()

# 双击表格中的行进行编辑
def on_item_double_click(event):
    selected_item = tree.selection()[0]
    task_values = tree.item(selected_item, 'values')
    
    entry_task.delete(0, "end")
    entry_task.insert(0, task_values[0])
    
    date_entry.set_date(datetime.strptime(task_values[1], '%Y-%m-%d'))
    status_var.set(task_values[2])
    
    app.selected_item = selected_item

# 保存编辑后的任务
def save_edit():
    if hasattr(app, 'selected_item'):
        selected_item = app.selected_item
        task = entry_task.get()
        deadline = date_entry.get_date().strftime('%Y-%m-%d')
        status = status_var.get()
        if task and deadline:
            tree.item(selected_item, values=(task, deadline, status))
            entry_task.delete(0, "end")
            date_entry.set_date(datetime.today())
            status_var.set("Pending")
            save_tasks()
            del app.selected_item

# 删除任务
def remove_task():
    selected_items = tree.selection()
    if selected_items:
        for item in selected_items:
            tree.delete(item)
        save_tasks()

# 模糊搜索任务
def search_tasks():
    query = entry_search.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    for task in all_tasks:
        if query in task[0].lower():
            tree.insert("", "end", values=task)

# 显示所有任务
def show_all_tasks():
    for row in tree.get_children():
        tree.delete(row)
    for task in all_tasks:
        tree.insert("", "end", values=task)

# 按截止日期排序
def sort_by_deadline():
    tasks = [(tree.item(item)['values'][0], tree.item(item)['values'][1], tree.item(item)['values'][2]) for item in tree.get_children()]
    sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x[1], '%Y-%m-%d'))
    for row in tree.get_children():
        tree.delete(row)
    for task in sorted_tasks:
        tree.insert("", "end", values=task)

# 保存任务列表到文件
def save_tasks():
    global all_tasks
    all_tasks = []
    for item in tree.get_children():
        all_tasks.append(tree.item(item, 'values'))
    with open(DATA_FILE, "w") as f:
        json.dump(all_tasks, f)

# 加载任务列表
def load_tasks():
    global all_tasks
    all_tasks = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            all_tasks = json.load(f)
            for task in all_tasks:
                tree.insert("", "end", values=task)

# 最小化到托盘
def minimize_to_tray():
    app.withdraw()  # 隐藏窗口
    show_tray_icon()

def show_tray_icon():
    # 创建托盘图标
    def on_quit(icon, item):
        icon.stop()
        app.quit()

    def on_show_window(icon, item):
        app.deiconify()  # 显示窗口
        icon.stop()

    # 创建一个简单的图标
    image = Image.new('RGB', (64, 64), color=(73, 109, 137))
    draw = ImageDraw.Draw(image)
    draw.rectangle((10, 10, 54, 54), fill="white")

    # 创建托盘图标和菜单
    icon = pystray.Icon("ToDoApp", image, menu=pystray.Menu(
        pystray.MenuItem('Show', on_show_window),
        pystray.MenuItem('Quit', on_quit)
    ))
    icon.run()

# 创建主窗口
app = ctk.CTk()
app.title("CliPg ToDo List")

# 获取屏幕宽高
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# 窗口尺寸设置
window_width = 470
window_height = 400

# 计算窗口位置，使其出现在右下角
position_right = screen_width +130
position_bottom = screen_height - 175

app.geometry(f"{window_width}x{window_height}+{position_right}+{position_bottom}")

# 输入框和按钮区域
frame_input = ctk.CTkFrame(app)
frame_input.pack(pady=10, padx=10, fill="x")

entry_task = ctk.CTkEntry(frame_input, placeholder_text="Enter your task here", width=180)
entry_task.grid(row=0, column=0, padx=5)

date_entry = DateEntry(frame_input, width=12, background="darkblue", foreground="white", borderwidth=2)
date_entry.grid(row=0, column=1, padx=5)

status_var = ctk.StringVar(value="Pending")
status_menu = ctk.CTkOptionMenu(frame_input, values=["Pending", "Completed"], variable=status_var, width=80)
status_menu.grid(row=0, column=2, padx=5)

add_button = ctk.CTkButton(frame_input, text="Add Task", command=add_task, width=70)
add_button.grid(row=0, column=3, padx=5)

save_edit_button = ctk.CTkButton(frame_input, text="Save Edit", command=save_edit, width=70)
save_edit_button.grid(row=0, column=4, padx=5)



# 搜索框和按钮区域
frame_search = ctk.CTkFrame(app)
frame_search.pack(pady=10, padx=10, fill="x")

entry_search = ctk.CTkEntry(frame_search, placeholder_text="Search tasks...", width=180)
entry_search.grid(row=0, column=0, padx=5)

search_button = ctk.CTkButton(frame_search, text="Search", command=search_tasks, width=70)
search_button.grid(row=0, column=1, padx=5)

show_all_button = ctk.CTkButton(frame_search, text="Show All", command=show_all_tasks, width=70)
show_all_button.grid(row=0, column=2, padx=5)

remove_button = ctk.CTkButton(frame_search, text="Remove Task", command=remove_task, width=70)
remove_button.grid(row=0, column=3, padx=5)

# 创建任务表格
columns = ("Task", "Deadline", "Status")
tree = ttk.Treeview(app, columns=columns, show="headings", height=10)
tree.heading("Task", text="Task")
tree.heading("Deadline", text="Deadline", command=sort_by_deadline)
tree.heading("Status", text="Status")

tree.column("Task", anchor="w", width=250)
tree.column("Deadline", anchor="center", width=100)
tree.column("Status", anchor="center", width=80)

style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 14))
style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))

tree.pack(pady=10, padx=10, fill="both", expand=True)

# 双击事件绑定
tree.bind("<Double-1>", on_item_double_click)

# 加载保存的任务
load_tasks()

# 窗口关闭时最小化到托盘
app.protocol("WM_DELETE_WINDOW", minimize_to_tray)

# 启动应用
app.mainloop()






















