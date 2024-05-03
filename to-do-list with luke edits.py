# Store Values in Shelf
# Open Values when App Starts
import tkinter as tk
from tkinter import messagebox
import json
from tkinter import ttk
from tkcalendar import Calendar

window = tk.Tk()
window.title("To-do List")

n = 0
# frame structure
frame00 = tk.Frame(window)
frame01 = tk.Frame(window)
frame10 = tk.Frame(window)
frame11 = tk.Frame(window)
frame20 = tk.Frame(window)
frame21 = tk.Frame(window)

frame00.grid(row=0, column=0)
frame01.grid(row=0, column=1)
frame10.grid(row=1, column=0)
frame11.grid(row=1, column=1)
frame20.grid(row=2, column=0)
frame21.grid(row=2, column=1)

tasks = {}
fixedEvents = {}
flexibleEvents = {}
#This is where new tasks go while program is running and
# before they are shelved
# I believe objects are being stored here because I ran a print function
# its length after adding a few.

newTaskLabel = tk.Label(text="Enter New Task:", master=frame01)
newTaskLabel.pack(side=tk.LEFT)
currentTasksLabel = tk.Label(text="Current Tasks", master=frame11)
currentTasksLabel.pack(side=tk.TOP)

flexibleTaskButton = tk.Button(master = frame11, text = 'Add Flexible Task')
fixedTaskButton = tk.Button(master = frame11, text = 'Add Fixed Event')
flexibleTaskButton.pack(side = tk.LEFT)
fixedTaskButton.pack(side = tk.LEFT)

notebook = ttk.Notebook(window)
notebook.grid(row=3, column=0, columnspan=2, sticky='ew')  # Adjust grid parameters as needed

# Create a Frame for flexible events
flexible_events_tab = tk.Frame(notebook)
notebook.add(flexible_events_tab, text="Flexible Events")

# Function to update the flexible events tab
def update_flexible_events_tab():
    # Clear current content in the tab
    for widget in flexible_events_tab.winfo_children():
        widget.destroy()

    # Add updated list of flexible events
    for key, value in flexibleEvents.items():
        tk.Label(flexible_events_tab, text=f"{value['name']} - {value['urgency']}").pack()

# Modify your saveFlexibleEvent function to call update_flexible_events_tab
def saveFlexibleEvent(event, urgency, task_name):
    task_details = f"{task_name} - {urgency}"
    # Assuming each flexible event is unique, you might use task_name as a unique key
    flexibleEvents[task_name] = {'urgency': urgency, 'name': task_name}
    print(flexibleEvents)
    event.widget.master.destroy()
    update_flexible_events_tab()  # Update the tab content after saving a new flexible event

# Rest of your functions and setup

# Initial update in case there are saved flexible events when the program starts
update_flexible_events_tab()

def loadOnOpen():
    """recalls shelf file when the program is opened and
 creates a checkbutton for each unchecked button. If the
 close function worked properly, the only checks in the file should
 be unchecked """
    try:
        with open('tasklist.json', 'r') as file:
            tasksToLoad = json.load(file)
            for title, info in tasksToLoad.items():
                if info.get('checked') == False:
                #"if not info.get('checked'):" worked because not being True is one thing equaling False is another
                    var = tk.IntVar()
                    newTaskBox = tk.Checkbutton(master = frame21, text =info.get('name'), variable = var, command=checkoffs)
                    newTaskBox.pack(side = tk.TOP)
                    tasks[newTaskBox] = var
                if title == 'FixedEvent':
                    print('Heyyyyy Bestie')
    except FileNotFoundError:
        print('No previous tasks found, starting New!')

def addFixedEvent(event):
    event_window = tk.Toplevel(window)
    event_window.title("Add Fixed Event")

    tk.Label(event_window, text="Event Name:").pack()
    event_name_entry = tk.Entry(event_window)
    event_name_entry.pack()

    tk.Label(event_window, text="Event Date:").pack()
    cal = Calendar(event_window, selectmode='day')
    cal.pack(pady=20)

    tk.Label(event_window, text="Event Time:").pack()
    time_var = tk.StringVar()
    time_dropdown = ttk.Combobox(event_window, textvariable=time_var, state="readonly")
    time_dropdown['values'] = [f"{hour:02d}:00" for hour in range(24)]  # 24-hour format
    time_dropdown.pack()

    def saveFixedEvent():
        task_name = event_name_entry.get()
        task_date = cal.get_date()
        task_time = time_var.get()
        task_details = f"{task_name} on {task_date} at {task_time}"
        fixedEvents['FixedEvent'] = {'name' : task_name, 'date': task_date, 'time': task_time, 'description' : task_details}
        # Following code makes fixed task appear on screen with simple tasks
        # task_box = tk.Checkbutton(master=frame_tasks, text=task_details, variable=var, command=checkoffs)
        # task_box.pack(side=tk.TOP)
        # tasks[task_box] = var
        # event_window.destroy()
        print(fixedEvents)
        time_dropdown.master.destroy()

    save_button = tk.Button(event_window, text="Save", command=saveFixedEvent)
    save_button.pack()

fixedTaskButton.bind('<Button-1>', addFixedEvent)

#Rework this format to something I understand better

def saveFlexibleEvent(event, urgency, task_name):
    task_details = f"{task_name} - {urgency}"
    flexibleEvents['Flexible'] = {'urgency': urgency, 'name': task_name}
    print(flexibleEvents)
    event.widget.master.destroy()


def addFlexibleEvent(event):
    event_window = tk.Toplevel(window)
    event_window.title("Add Time Flexible Event")

    tk.Label(event_window, text="Event Name:").pack()
    event_name_entry = tk.Entry(event_window)
    event_name_entry.pack()

    urgency_levels = ["Urgent", "Important", "Whenever"]
    for level in urgency_levels:
        flexible_task_button = tk.Button(event_window, text=level)
        flexible_task_button.pack()

        flexible_task_button.bind('<Button-1>', lambda event=event, level=level: saveFlexibleEvent(event, level, event_name_entry.get()))

flexibleTaskButton.bind('<Button-1>', addFlexibleEvent)

def newTaskFunction(event):
    """ creates a checkbutton when user types new task
and presses <enter> (bound to <return?>"""
    newTaskName = newTaskEntry.get()
    var = tk.IntVar()
    newTaskBox = tk.Checkbutton(
        master=frame21, text=newTaskName, variable=var, command=checkoffs
    )
    newTaskBox.pack(side=tk.TOP)
    tasks[newTaskBox] = var
    newTaskEntry.delete(0, tk.END)


def checkoffs():
    """ destroys checkbutton objects after they've
been checked off"""
    # Could this be simplified since only one box will ever
    # be checked at a time?
    destroyList = []
    for i, v in tasks.items():
        if v.get() == 1:
            destroyList.append(i)

    for item in destroyList:
        item.destroy()


def finalSave():
    """ Supposed to save remaining boxes (unchecked), when
user X's out of window """

    savedTasks = {}
    savedFixedEvents = {}

    with open('tasklist.json', 'w') as file:
        for widget, v in tasks.items():
            if v.get() == 0:
                task_name = widget.cget('text')
                savedTasks[task_name] = {"name": task_name, "checked": False}

        for event, v in fixedEvents.items():
            savedFixedEvents[event] = v

        savedTasks.update(savedFixedEvents)

        json.dump(obj = savedTasks, fp = file)

    window.destroy()


newTaskEntry = tk.Entry(frame01)
newTaskEntry.pack()
newTaskEntry.bind("<Return>", newTaskFunction)

window.protocol("WM_DELETE_WINDOW", finalSave)

print(tasks)

loadOnOpen()

tk.mainloop()
