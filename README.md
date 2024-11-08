# ToDoList

## Intro
基于python的构建的简易ToDoList桌面应用，便于提醒和管理你的任务。

A simple ToDoList desktop application built based on python, for reminding and managing your tasks.


## Show

![](./img/example1.png)



## Functions

- **Add Task**
  可以直接在日期旁的输入框写入你想添加的任务和任务截止日期，任务信息会持久化在一个json文件中。

  You can write your task and deadline in the input box next to the date. The task information will be persisted in a json file.



- **Remove Task**
  点击你想删除的任务，再点击remove task即可删除。

  Click the task you want to delete, and then click remove task to delete it.


- **Save Edit**
  双击任务，可以修改内容或日期，再点击save edit即可保存修改。

  Double-click the task to modify the content or deadline, and then click save edit to save the modification.


- **Pending**
  完成状态，目前来看好像没什么用，因为一般完成任务后直接remove了。

  Completed status, currently it seems to have no use, because generally completed tasks are directly removed.


- **Search**
  支持模糊搜索

  Support fuzzy search

- **Show All**
  展示所有任务，用于配合搜索后，返回原来的任务列表。但是给搜索内容删除后，在点击search也可以直接返回。

  Show all tasks, used to return to the original task list after searching. But after deleting the search content, you can also directly return to the original task list by clicking search.

- **Others**
  - 点击Deadline可以按照截止时间排序

    Click Deadline to sort by deadline

  - 支持开机自启，可能会有点慢，而且还会弹出命令行和记事本
  
    Support auto startup, it may be a bit slow, and it will also pop up the command line and the note pad



## Requirements

- python3
- Windows



## Start

你需要把`start_todo.bat`文件放在下面目录中

You need to put the `start_todo.bat` file in the following directory:

```
C:\Users\your_username\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```



修改start_todo.bat启动脚本

Modify the start_todo.bat startup script

```
@echo off
cd D:\your_file  //MyToDo.py的文件位置  MyToDo.py file location
pythonw "D:\your_file\MyToDo.py"
```



重启电脑或直接在命令行输入上面命令即可启动。

Restart the computer or directly enter the above command to start it.



## Extra

如果你有任何想法和修改建议可以联系我!

If you have any ideas and modification suggestions, please contact me!