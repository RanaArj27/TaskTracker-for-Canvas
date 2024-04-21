# Imports CTK library for UI development, WebBrowser for opening URLs,
# Pytz for converting datetime objects to GMT time, CanvasAPI for accessing
# Canvas courses and assignments, and DateTime to use datetime objects
import customtkinter as ctk, webbrowser, time, pytz
from canvasapi import Canvas
from datetime import datetime


def clear_frame(frame):
    # hides all widgets from frame
    for widget in frame.winfo_children():
        widget.pack_forget()

#Sets the appearance/size of the UI window

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
root = ctk.CTk()
root.geometry("950x575")
root.title('TaskTracker v1.0')

global frame
frame = ctk.CTkScrollableFrame(master=root)
frame.pack(pady = 20, padx = 60, fill = "both", expand = True)


#prints the title
global title
title=ctk.CTkLabel(master=frame, text="Login to Canvas", font=("Convection", 30))
title.pack(pady=12, padx=10)
#prints the instructions for the user
global domain
directions=ctk.CTkLabel(master=frame, text="Enter your Canvas domain below WITH https (ex. https://issaquah.instructure.com for ISD)", font=("Convection", 18))
directions.pack(pady=10,padx=12)
url=ctk.CTkEntry(master=frame, placeholder_text="Enter your Canvas domain:", font=("Convection", 18), width=250, height=50)
url.pack(pady=12,padx=10)
domain=url.get()
domain=str(domain)
global instructions
instructions=ctk.CTkLabel(master=frame, text="Please type/paste your Canvas access token below", font=("Convection", 18))
instructions.pack(pady=12, padx=10)
global instructions1
instructions1=ctk.CTkLabel(master=frame, text="Save the token where you can remember it, and make sure it's correct, or you'll have to make another one", font=("Convection", 15))
instructions1.pack(pady=12, padx=10)
#generates a text box which prompts the user for their canvas api access token
global token
entertoken=ctk.CTkEntry(master=frame, placeholder_text="Type token here:", width=400, height=50, font=("Convection",15))
entertoken.pack(pady=12, padx=10)


#remember=ctk.CTkSwitch(master=frame, text="Remember Me", font=("Convection", 12))
#remember.pack(pady=12, padx=10)
def display_pending_assignments(domain):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    canvas = Canvas(domain, entertoken.get())
    courses = canvas.get_courses(enrollment_state="active")
    clear_frame(frame)
    
    for course in courses:
        try:
            filtered_assignments = list(filter(lambda assignment: assignment.due_at is not None and
                                                pytz.timezone("America/Vancouver").localize(datetime.now()) <
                                                datetime.strptime(assignment.due_at, "%Y-%m-%dT%H:%M:%S%z").replace(
                                                    tzinfo=pytz.timezone("America/Vancouver")),
                                                list(course.get_assignments())))

            # The list we are iterating contains all of the assignments in the course, filtered to only include ones that are due in the future
            for assignment in filtered_assignments:
                assignment_date_time = datetime.strptime(assignment.due_at, "%Y-%m-%dT%H:%M:%S%z").replace(
                    tzinfo=pytz.UTC).astimezone(pytz.timezone("America/Vancouver"))

                # Create a label for the assignment
                assignment_text = f"{course.name}: {assignment.name}, due by {months[assignment_date_time.month - 1]} {assignment_date_time.day}, {assignment_date_time.year} at {assignment_date_time.hour:02}:{assignment_date_time.minute:02} PDT"
                assignment_label = ctk.CTkLabel(master=frame, text=assignment_text, font=("Convection", 15))
                assignment_label.pack(pady=5, padx=10)

        except Exception as e:
            print(f"Error: {e}")
            continue

print(domain)
submit = ctk.CTkButton(master=frame, text="Submit", font=("Convection", 15), command=lambda: display_pending_assignments("https://issaquah.instructure.com"))
submit.pack(pady=12, padx=10)

def open_tutorial():
    webbrowser.open_new("https://www.youtube.com/watch?v=cZ5cn8stjM0")
tutorial=ctk.CTkButton(master=frame, text="How to find your access token (3rd party YT tutorial)", font=("Convection", 10), command= open_tutorial)
tutorial.pack(pady=12, padx=10)



def add_assignment():
    # Create entry widgets
    global taskname
    global taskname_entry
    global taskdue_entry
    global taskdue
    
    taskname_entry=ctk.CTkEntry(master=frame, placeholder_text="Enter task name", font=("Convection", 10))
    taskname_entry.pack(pady=12,padx=10)
    taskdue_entry=ctk.CTkEntry(master=frame, placeholder_text="Enter due date", font=("Convection", 10))
    taskdue_entry.pack(pady=12,padx=10)
    addTask=ctk.CTkButton(master=frame, text="Add", command=add_task)
    addTask.pack(pady=12,padx=10)
    global tasks
    tasks = []  # List to store tasks
    




def add_task():   
    taskname = taskname_entry.get()
    taskdue = taskdue_entry.get()

    print("taskName:"+ taskname + "taskDue:" + taskdue)
    if taskname and taskdue:
        tasks.append({"name": taskname, "due_date": taskdue})
        taskname_entry.delete(0, ctk.END)  # Clear the entry box
        taskdue_entry.delete(0, ctk.END)  # Clear the entry box
        
    else:
        error=ctk.CTkLabel(master=frame, text="Error: Please enter both task name and due date.")
   
    
    task = tasks[-1]
    name=ctk.CTkLabel(master=frame, text=(f"Name: {taskname}, Due Date: {taskdue}"), font=("Convection", 22))
    name.pack(pady=12,padx=10)

        
manual=ctk.CTkButton(master=frame, text="Add assignments manually", font=("Convection", 13), command= add_assignment)
manual.pack(pady=12,padx=10)

manualTaskHeading=ctk.CTkLabel(master=frame, text="Current tasks:", font=("Convection", 19))
manualTaskHeading.pack(pady=12,padx=10)





root.mainloop()