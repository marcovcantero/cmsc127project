from datetime import datetime
from dateutil import parser
import mysql.connector as mariadb

# establish connection to mariadb database
db = mariadb.connect(
    host='localhost', 
    user='user1', 
    password='12345678',
    database="task_db"
)

cursor = db.cursor(buffered=True)

# create database and tables
def validateDateFormat(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        print("Invalid date. Date format should be YYYY-MM-DD.")
        return False
    
def validateDate(date1, date2):
    try:
        date1 = parser.parse(date1)
        date2 = parser.parse(date2)
        dateDiff = date2 - date1
        if dateDiff.days >= 0:
            return True
    except:
        return False
        
    
def checkDatabase():
    cursor.execute("SELECT * FROM task")
    record = cursor.fetchone()
    if not record:
        print("\nThere are no tasks.")
        return False
    else:
        return True

def addTask(db, cursor):
    try:
        while True:
            taskTitle = input("\nEnter new task title: ")
            if taskTitle != "":
                break
            else:
                print("\nTask title must not be empty.")
        while True:
            dateCreated = input("\nEnter date created (YYYY-MM-DD): ")
            if dateCreated != "":
                if validateDateFormat(dateCreated) == True:
                    break
            else:
                print("\nDate created must not be empty.")
        while True:
            deadline = input("\nEnter deadline (YYYY-MM-DD): ")
            if deadline != "":
                if validateDateFormat(deadline) == True:
                    if validateDate(dateCreated, deadline) == True:
                        break
                    else:
                        print("\nInvalid deadline. Deadline must not be before the date created.")
            else:
                print("\nDeadline must not be empty.")
        taskDescription = input("Enter task description: ")
        cursor.execute("INSERT INTO task (task_title, date_created, deadline, task_description) VALUES (%s, %s, %s, %s)", (taskTitle, dateCreated, deadline, taskDescription))
        db.commit()
        print("\nAdded task successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to add task. Error: {e}")
        
def editTaskTitle(db, cursor):
    try:
        if checkDatabase() == False:
            return
        taskNo = input("\nEnter task number: ")
        # check if taskNo exists first in database, if not return from function
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record = cursor.fetchone()
        if not record:
            print("\nThere are no tasks that match.")
            return
        while True:
            taskTitle = input("\nEnter new task title: ")
            if taskTitle != "":
                break
            else:
                print("\nTask title must not be empty.")
        cursor.execute("UPDATE task SET task_title = %s WHERE taskno = %s", (taskTitle, taskNo))
        db.commit()
        print("\nEdited task title successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to edit task title. Error: {e}")
        
def editDateCreated(db, cursor):
    try:
        if checkDatabase() == False:
            return
        taskNo = input("\nEnter task number: ")
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record = cursor.fetchone()
        deadline = str(record[3])
        dateCompleted = str(record[4])
        if not record:
            print("\nThere are no tasks that match.")
            return
        while True:
            dateCreated = input("\nEnter new date created (YYYY-MM-DD): ")
            if dateCreated != "":
                if validateDateFormat(dateCreated) == True:
                    if validateDate(dateCreated, deadline) == True:
                        if dateCompleted != "None":
                            if validateDate(dateCreated, dateCompleted) == True:
                                break
                            else:
                                print("\nInvalid date created. Date created must not be after the date completed.")
                        else:
                            break
                    else:
                        print("\nInvalid date created. Date created must not be after the deadline.")
            else:
                print("\nDate created must not be empty.")
        cursor.execute("UPDATE task SET date_created = %s WHERE taskno = %s", (dateCreated, taskNo))
        db.commit()
        print("\nEdited date created successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to edit date created. Error: {e}")
        
def editDeadline(db, cursor):
    try:
        if checkDatabase() == False:
            return
        taskNo = input("\nEnter task number: ")
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record = cursor.fetchone()
        dateCreated = str(record[2])
        if not record:
            print("\nThere are no tasks that match.")
            return
        while True:
            deadline = input("\nEnter new deadline (YYYY-MM-DD): ")
            if deadline != "":
                if validateDateFormat(deadline) == True:
                    if validateDate(dateCreated, deadline) == True:
                        break
                    else:
                        print("\nInvalid deadline. Deadline must not be before the date created.")
            else:
                print("\nDeadline must not be empty.")
        cursor.execute("UPDATE task SET deadline = %s WHERE taskno = %s", (deadline, taskNo))
        db.commit()
        print("\nEdited deadline successfully.")
        
    except mariadb.Error as e:
        print(F"Failed to edit deadline. Error: {e}")
        
def editDateCompleted(db, cursor):
    try:
        if checkDatabase() == False:
            return
        taskNo = input("\nEnter task number: ")
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record = cursor.fetchone()
        dateCreated = str(record[2])
        if not record:
            print("\nThere are no tasks that match.")
            return
        while True:
            dateCompleted = input("\nEnter new date completed (YYYY-MM-DD): ")
            if validateDateFormat(dateCompleted) == True:
                if validateDate(dateCreated, dateCompleted) == True:
                    break
                else:
                    print("\nInvalid date completed. Date completed must not be before the date created.")
        cursor.execute("UPDATE task SET date_completed = %s WHERE taskno = %s", (dateCompleted, taskNo))
        db.commit()
        print("\nEdited date completed successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to edit date completed. Error: {e}")
        
def editTaskDescription(db, cursor):
    try:
        if checkDatabase() == False:
            return
        taskNo = input("\nEnter task number: ")
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record = cursor.fetchone()
        if not record:
            print("\nThere are no tasks that match.")
            return
        taskDescription = input("Enter new task description: ")
        cursor.execute("UPDATE task SET task_description = %s WHERE taskno = %s", (taskDescription, taskNo))
        db.commit()
        print("\nEdited task description successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to edit task description. Error: {e}")
        
def deleteTask(db, cursor):
    try:
        if checkDatabase() == False:
            return
        taskNo = input("\nEnter task number: ")
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record = cursor.fetchone()
        if not record:
            print("\nThere are no tasks that match.")
            return
        cursor.execute("DELETE FROM task WHERE taskno = %s", (taskNo,))
        # sorts the taskno after deleting a task
        cursor.execute("SET @count = 0")
        cursor.execute("UPDATE task SET taskno = @count:= @count + 1")
        cursor.execute("ALTER TABLE task AUTO_INCREMENT = 1")
        db.commit()
        print("\nDeleted task successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to delete task. Error: {e}")
        
def viewAllTask():
    try:
        cursor.execute("SELECT * FROM task")
        data = cursor.fetchall()
        if not data:
            print("\nThere are no tasks left to do. Congratulations!")
            return
        print("\nTotal number of tasks: ", cursor.rowcount)
        print("\nTo-Do List")
        for row in data:
            print("\nTask No. ", row[0])
            print("Task Title: ", row[1])
            print("Date Created: ", row[2])
            print("Deadline: ", row[3])
            print("Date Completed: ", row[4])
            print("Task Description: ", row[5])
            print("Task Status (0 - Ongoing, 1 - Finished): ", row[6])
    
    except mariadb.Error as e:
        print(f"Failed to view all tasks. Error: {e}")

def editOptions(option):
    match option:
        case '1':
            editTaskTitle(db, cursor)
        case '2':
            editDateCreated(db, cursor)
        case '3':
            editDeadline(db, cursor)
        case '4':
            editDateCompleted(db, cursor)
        case '5':
            editTaskDescription(db, cursor)
        case '0':
            main()
        case _:
            print("\nInvalid input.")

# app loop which matches choice to its corresponding action
def app_loop(choice):
    while choice != 0:
        match choice:
            case '1':
                addTask(db, cursor)
            case '2':
                print('\n------EDIT TASK------', '[1] Edit Task Title', '[2] Edit Date Created', '[3] Edit Deadline', '[4] Edit Date Completed', '[5] Edit Task Description', '[0] Back', sep='\n')
                option = input("\nEdit option: ")
                editOptions(option)
            case '3':
                deleteTask(db, cursor)
            case '4':
                viewAllTask()
            case '5':
                print("Editing task!")
            case '6':
                print("Deleting task!")
            case '7':
                print("Adding task!")
            case '8':
                print("Editing task!")
            case '9':
                print("Viewing Category!")
            case '10':
                print("Adding task to a Category!")
            case '11':
                print("Viewing task!")
            case '0':
                cursor.close()
                db.close()
                print("\nExiting app!")
                quit()
            case _:
                print("\nInvalid input.")
        print('\n------TO-DO APP------', '[1] Add/Create Task', '[2] Edit Task', '[3] Delete Task', '[4] View All Tasks', '[5] Mark Task as done', '[6] Add Category', '[7] Edit Category', '[8] Delete Category', '[9] View Category', '[10] Add a Task to a Category', '[11] View Task (per day, month)', '[0] Exit', sep='\n')
        choice = input("\nChoice: ")
        
def main():
    print('\n------TO-DO APP------', '[1] Add/Create Task', '[2] Edit Task', '[3] Delete Task', '[4] View All Tasks', '[5] Mark Task as done', '[6] Add Category', '[7] Edit Category', '[8] Delete Category', '[9] View Category', '[10] Add a Task to a Category', '[11] View Task (per day, month)', '[0] Exit', sep='\n')
    choice = input("\nChoice: ")
    app_loop(choice)

main()