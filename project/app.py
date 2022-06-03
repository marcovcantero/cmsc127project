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
        
    
def checkTasks():
    cursor.execute("SELECT * FROM task")
    record = cursor.fetchone()
    if not record:
        print("\nThere are no tasks.")
        return False
    else:
        return True

def checkCategory():
    cursor.execute("SELECT * FROM category")
    record = cursor.fetchone()
    if not record:
        print("\nThere are no categories.")
        return False
    else:
        return True

def addTask(db, cursor):
    try:
        while True:
            print("\nEnter 0 to cancel.")
            taskTitle = input("\nEnter new task title: ")
            if taskTitle != "":
                break
            else:
                print("\nTask title must not be empty.")
        if taskTitle == "0":
                return
        while True:
            print("\nEnter 0 to cancel.")
            dateCreated = input("\nEnter date created (YYYY-MM-DD): ")
            if dateCreated != "":
                if validateDateFormat(dateCreated) == True:
                    break
            else:
                print("\nDate created must not be empty.")
        if dateCreated == "0":
                return
        while True:
            print("\nEnter 0 to cancel.")
            deadline = input("\nEnter deadline (YYYY-MM-DD): ")
            if deadline != "":
                if validateDateFormat(deadline) == True:
                    if validateDate(dateCreated, deadline) == True:
                        break
                    else:
                        print("\nInvalid deadline. Deadline must not be before the date created.")
            else:
                print("\nDeadline must not be empty.")
        if deadline == "0":
                return
        while True:
            print("\nEnter 0 to cancel.")
            taskDescription = input("\nEnter task description: ")
            if taskDescription != "":
                break
            else:
                print("\nTask description must not be empty.")
        if taskDescription == "0":
                return
        cursor.execute("INSERT INTO task (task_title, date_created, deadline, task_description) VALUES (%s, %s, %s, %s)", (taskTitle, dateCreated, deadline, taskDescription))
        db.commit()
        cursor.execute("SELECT * FROM task ORDER BY taskno DESC LIMIT 1")
        record = cursor.fetchone()
        print(f"\nAdded task #{str(record[0])} {taskTitle} successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to add task. Error: {e}")
        
def editTaskTitle(db, cursor):
    try:
        if checkTasks() == False:
            return
        while True:
            print("\nEnter 0 to cancel.")
            taskNo = input("\nEnter task number: ")
            if taskNo != "":
                break
            else:
                "\nTask number must not be empty."
        if taskNo == "0":
            return
        # check if taskNo exists first in database, if not return from function
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record = cursor.fetchone()
        if not record:
            print("\nThere are no tasks that match.")
            return
        while True:
            print("\nEnter 0 to cancel.")
            taskTitle = input("\nEnter new task title: ")
            if taskTitle != "":
                break
            else:
                print("\nTask title must not be empty.")
        if taskTitle == "0":
                return
        cursor.execute("UPDATE task SET task_title = %s WHERE taskno = %s", (taskTitle, taskNo))
        db.commit()
        print(f"\nEdited title of task #{taskNo} to {taskTitle} successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to edit task title. Error: {e}")
        
def editDateCreated(db, cursor):
    try:
        if checkTasks() == False:
            return
        while True:
            print("\nEnter 0 to cancel.")
            taskNo = input("\nEnter task number: ")
            if taskNo != "":
                break
            else:
                "\nTask number must not be empty."
        if taskNo == "0":
            return
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record = cursor.fetchone()
        deadline = str(record[3])
        dateCompleted = str(record[4])
        if not record:
            print("\nThere are no tasks that match.")
            return
        while True:
            print("\nEnter 0 to cancel.")
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
            elif dateCreated == "0":
                return
            else:
                print("\nDate created must not be empty.")
        if dateCreated == "0":
                return
        cursor.execute("UPDATE task SET date_created = %s WHERE taskno = %s", (dateCreated, taskNo))
        db.commit()
        print(f"\nEdited date created of task #{taskNo} to {dateCreated} successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to edit date created. Error: {e}")
        
def editDeadline(db, cursor):
    try:
        if checkTasks() == False:
            return
        while True:
            print("\nEnter 0 to cancel.")
            taskNo = input("\nEnter task number: ")
            if taskNo != "":
                break
            else:
                "\nTask number must not be empty."
        if taskNo == "0":
            return
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record = cursor.fetchone()
        dateCreated = str(record[2])
        if not record:
            print("\nThere are no tasks that match.")
            return
        while True:
            print("\nEnter 0 to cancel.")
            deadline = input("\nEnter new deadline (YYYY-MM-DD): ")
            if deadline != "":
                if validateDateFormat(deadline) == True:
                    if validateDate(dateCreated, deadline) == True:
                        break
                    else:
                        print("\nInvalid deadline. Deadline must not be before the date created.")
            elif deadline == "0":
                return
            else:
                print("\nDeadline must not be empty.")
        if deadline == "0":
                return
        cursor.execute("UPDATE task SET deadline = %s WHERE taskno = %s", (deadline, taskNo))
        db.commit()
        print(f"\nEdited deadline of task #{taskNo} to {deadline} successfully.")
        
    except mariadb.Error as e:
        print(F"Failed to edit deadline. Error: {e}")
        
def editDateCompleted(db, cursor):
    try:
        if checkTasks() == False:
            return
        while True:
            print("\nEnter 0 to cancel.")
            taskNo = input("\nEnter task number: ")
            if taskNo != "":
                break
            else:
                "\nTask number must not be empty."
        if taskNo == "0":
            return
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record = cursor.fetchone()
        dateCreated = str(record[2])
        if not record:
            print("\nThere are no tasks that match.")
            return
        while True:
            print("\nEnter 0 to cancel.")
            dateCompleted = input("\nEnter new date completed (YYYY-MM-DD): ")
            if dateCompleted != "":
                if validateDateFormat(dateCompleted) == True:   
                    if validateDate(dateCreated, dateCompleted) == True:
                        break
                    else:
                        print("\nInvalid date completed. Date completed must not be before the date created.")
            elif dateCompleted == "0":
                return
            else:
                print("\nDate completed must not be empty.")
        if dateCompleted == "0":
                return
        cursor.execute("UPDATE task SET date_completed = %s WHERE taskno = %s", (dateCompleted, taskNo))
        db.commit()
        print(f"\nEdited date completed of task #{taskNo} to {dateCompleted} successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to edit date completed. Error: {e}")
        
def editTaskDescription(db, cursor):
    try:
        if checkTasks() == False:
            return
        while True:
            print("\nEnter 0 to cancel.")
            taskNo = input("\nEnter task number: ")
            if taskNo != "":
                break
            else:
                "\nTask number must not be empty."
        if taskNo == "0":
            return
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record = cursor.fetchone()
        if not record:
            print("\nThere are no tasks that match.")
            return
        while True:
            print("\nEnter 0 to cancel.")
            taskDescription = input("Enter new task description: ")
            if taskDescription != "":
                break
            else:
                "\nTask description must not be empty."
        cursor.execute("UPDATE task SET task_description = %s WHERE taskno = %s", (taskDescription, taskNo))
        db.commit()
        print(f"\nEdited description of task #{taskNo} to {taskDescription} successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to edit task description. Error: {e}")
        
def deleteTask(db, cursor):
    try:
        if checkTasks() == False:
            return
        while True:
            print("\nEnter 0 to cancel.")
            taskNo = input("\nEnter task number: ")
            if taskNo != "":
                break
            else:
                "\nTask number must not be empty."
        if taskNo == "0":
            return
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record = cursor.fetchone()
        if not record:
            print("\nThere are no tasks that match.")
            return
        cursor.execute("DELETE FROM task WHERE taskno = %s", (taskNo,))
        cursor.execute("DELETE FROM belongsto WHERE taskno = %s", (taskNo,))
        # sorts the taskno after deleting a task
        cursor.execute("SET @count = 0")
        cursor.execute("UPDATE task SET taskno = @count:= @count + 1")
        cursor.execute("ALTER TABLE task AUTO_INCREMENT = 1")
        db.commit()
        print(f"\nDeleted task #{taskNo} successfully.")
        
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
            print(f"\nTask #{row[0]}")
            print(f"Task Title: {row[1]}")
            print(f"Date Created: {row[2]}")
            print(f"Deadline: {row[3]}")
            print(f"Date Completed: {row[4]}")
            print(f"Task Description: {row[5]}")
            print(f"Task Status (0 - Ongoing, 1 - Finished): {row[6]}")
    
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
#add category
def addCategory(db, cursor):
    try:
        while True:
            print("\nEnter 0 to cancel.")
            categoryName = input("\nEnter category name: ")
            if categoryName != "":
                break
            else:
                print("\nCategory name must not be empty.")
        if categoryName == "0":
                return
        cursor.execute("INSERT INTO category (categoryname) VALUES (%s)", (categoryName,))
        db.commit()
        cursor.execute("SELECT * FROM category ORDER BY categoryno DESC LIMIT 1")
        record = cursor.fetchone()
        print(f"\nAdded category #{str(record[0])} {categoryName} successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to add category. Error: {e}")
    
#edit category name
def editCategoryName(db, cursor):
    try:
        if checkCategory() == False:
            return
        while True:
            print("\nEnter 0 to cancel.")
            categoryNo = input("\nEnter category number: ")
            if categoryNo != "":
                break
            else:
                print("\nCategory number must not be empty.")
        if categoryNo == "0":
                return
        # check if categoryNo exists first in database, if not return from function
        cursor.execute("SELECT * FROM category WHERE categoryno = %s", (categoryNo,))
        record = cursor.fetchone()
        if not record:
            print("\nThere are no categories that match.")
            return
        while True:
            print("\nEnter 0 to cancel.")
            categoryName = input("Enter new category name: ")
            if categoryName != "":
                break
            else:
                print("\nCategory name must not be empty.")
        if categoryName == "0":
                return        
        cursor.execute("UPDATE category SET categoryname = %s WHERE categoryno = %s", (categoryName, categoryNo))
        db.commit()
        print(f"\nEdited name of category #{categoryNo} to {categoryName} successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to edit category name. Error: {e}")

#delete category
def deleteCategory(db, cursor):
    try:
        if checkCategory() == False:
            return
        while True:
            print("\nEnter 0 to cancel.")
            categoryNo = input("\nEnter category number: ")
            if categoryNo != "":
                break
            else:
                "\nCategory number must not be empty."
        if categoryNo == "0":
                return
        cursor.execute("SELECT * FROM category WHERE categoryno = %s", (categoryNo,))
        record = cursor.fetchone()
        if not record:
            print("\nThere are no categories that match.")
            return
        cursor.execute("DELETE FROM category WHERE categoryno = %s", (categoryNo,))
        # sorts the categoryno after deleting a category
        cursor.execute("SET @count = 0")
        cursor.execute("UPDATE category SET categoryno = @count:= @count + 1")
        cursor.execute("ALTER TABLE category AUTO_INCREMENT = 1")
        db.commit()
        print(f"\nDeleted category #{categoryNo} {str(record[1])} successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to delete category. Error: {e}")

#view category
def viewCategory():
    try:
        if checkCategory() == False:
            return
        cursor.execute("SELECT * FROM category")
        record1 = cursor.fetchall()
        for row in record1:
            print(f"\nCategory #{row[0]}")
            print(f"Category Name: {row[1]}")
        while True:
            print("\nEnter 0 to cancel.")
            categoryNo = input("\nEnter category number: ")
            if categoryNo != "":
                break
            else:
                "\nCategory number must not be empty."
        if categoryNo == "0":
                return
        cursor.execute("SELECT * FROM category WHERE categoryno = %s", (categoryNo,))
        record2 = cursor.fetchone()
        if not record2:
            print("\nThere are no categories that match.")
            return
        print(f"\nCATEGORY: {str(record2[1])}")
        cursor.execute("SELECT * FROM task WHERE taskno IN (SELECT taskno FROM belongsto WHERE categoryno = %s)", (categoryNo,))
        data = cursor.fetchall()
        if not data:
            print("\nThere are no tasks in this category.")
            return
        print("\nTotal number of tasks in this category: ", cursor.rowcount)
        print("\nTo-Do List")
        for row in data:
            print(f"\nTask #{row[0]}")
            print(f"Task Title: {row[1]}")
            print(f"Date Created: {row[2]}")
            print(f"Deadline: {row[3]}")
            print(f"Date Completed: {row[4]}")
            print(f"Task Description: {row[5]}")
            print(f"Task Status (0 - Ongoing, 1 - Finished): {row[6]}")
    
    except mariadb.Error as e:
        print(f"Failed to view category. Error: {e}")

# mark Task as Done
def markTaskAsDone(db, cursor):
    try:
        if checkTasks() == False:
            return
        while True:
            print("\nEnter 0 to cancel.")
            taskNo = input("\nEnter task number: ")
            if taskNo != "":
                break
            else:
                "\nTask number must not be empty."
        if taskNo == "0":
                return
        # check if taskNo exists first in database, if not return from function
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record = cursor.fetchone()
        if not record:
            print("\nThere are no tasks that match.")
            return
        taskStatus = str(record[6])
        while True:
            if taskStatus == "0":
                cursor.execute("UPDATE task SET date_Completed = CURDATE(), task_status = 1 WHERE taskno = %s", (taskNo,))
                break
            else:
                print(f"\nTask #{taskNo} is already marked as done.")
                break
        db.commit()
        print(f"\nTask #{taskNo} is marked as done.")

    except mariadb.Error as e:
        print(f"Failed to mark the task as done. Error: {e}")

# Add a Task to a Category
def addTasktoCategory(db, cursor):
    try:
        if checkTasks() == False:
            return
        while True:
            print("\nEnter 0 to cancel.")
            taskNo = input("\nEnter task number: ")
            if taskNo != "":
                break
            else:
                "\nTask number must not be empty."
        if taskNo == "0":
                return
        # check if taskNo exists first in database, if not return from function
        cursor.execute("SELECT * FROM task WHERE taskno = %s", (taskNo,))
        record1 = cursor.fetchone()
        if not record1:
            print("\nThere are no tasks that match.")
            return
        while True:
            print("\nEnter 0 to cancel.")
            categoryNo = input("\nEnter category number: ")
            if categoryNo != "":
                break
            else:
                "\nCategory number must not be empty."
        if categoryNo == "0":
                return
        # check if categoryNo exists first in database, if not return from function
        cursor.execute("SELECT * FROM category WHERE categoryno = %s", (categoryNo,))
        record2 = cursor.fetchone()
        if not record2:
            print("\nThere are no categories that match.")
            return
        categoryName = str(record2[1])
        cursor.execute("INSERT INTO belongsto VALUES (%s, %s)", (taskNo, categoryNo))
        db.commit()
        print(f"\nAdded task #{taskNo} to category #{categoryNo} {categoryName} successfully.")
        
    except mariadb.Error as e:
        print(f"Failed to add task to category. Error: {e}")

# view task per day or month depending on user input
def viewOptions(option):
    match option:
        case '1':
            viewTaskPerDay()
        case '2':
            viewTaskPerMonth()
        case '0':
            main()
        case _:
            print("\nInvalid input.")

#View Task per Day
def viewTaskPerDay():
    try:
        if checkTasks() == False:
            return
        while True:
            print("\nEnter 0 to cancel.")
            date = input("\nEnter date of tasks to be viewed (YYYY-MM-DD): ")
            if date != "":
                if validateDateFormat(date) == True:
                    break
            elif date == "0":
                break
            else:
                print("\nDate created must not be empty.")
        if date == "0":
                return
        cursor.execute("SELECT * FROM task WHERE deadline = %s", (date,))
        data = cursor.fetchall()
        if not data:
            print("\nThere are no tasks for this date.")
            return
        print("\nTotal number of tasks: ", cursor.rowcount)
        print("\nTo-Do List")
        for row in data:
            print(f"\nTask #{row[0]}")
            print(f"Task Title: {row[1]}")
            print(f"Date Created: {row[2]}")
            print(f"Deadline: {row[3]}")
            print(f"Date Completed: {row[4]}")
            print(f"Task Description: {row[5]}")
            print(f"Task Status (0 - Ongoing, 1 - Finished): {row[6]}")
    except mariadb.Error as e:
        print(f"Failed to add task to category. Error: {e}")

#View Task per Month
def viewTaskPerMonth():
    try:
        if checkTasks() == False:
            return
        while True:
            print("\nEnter 0 to cancel.")
            date = input("\nEnter year and month number of tasks to be viewed (YYYY-MM): ")
            if date != "" :
                try:
                    datetime.strptime(date, "%Y-%m")
                    break
                except ValueError:
                    print("\nInvalid year and month. Year and month format should be YYYY-MM.")
            elif date == "0":
                return
            else:
                print("\nYear and month number must not be empty.")
        if date == "0":
                return
        cursor.execute("SELECT * FROM task WHERE deadline LIKE %s", (date + "%",))
        data = cursor.fetchall()
        if not data:
            print("\nThere are no tasks for this specific month and year.")
            return
        print("\nTotal number of tasks: ", cursor.rowcount)
        print("\nTo-Do List")
        for row in data:
            print(f"\nTask #{row[0]}")
            print(f"Task Title: {row[1]}")
            print(f"Date Created: {row[2]}")
            print(f"Deadline: {row[3]}")
            print(f"Date Completed: {row[4]}")
            print(f"Task Description: {row[5]}")
            print(f"Task Status (0 - Ongoing, 1 - Finished): {row[6]}")
    except mariadb.Error as e:
        print(f"Failed to view tasks. Error: {e}")

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
                markTaskAsDone(db, cursor)
            case '6':
                addCategory(db, cursor)
            case '7':
                editCategoryName(db, cursor)
            case '8':
                deleteCategory(db, cursor)
            case '9':
                viewCategory()
            case '10':
                addTasktoCategory(db, cursor)
            case '11':
                print('\n------VIEW TASK PER DAY, MONTH------', '[1] View Task per Day', '[2] View Task per Month', '[0] Back', sep='\n')
                option = input("\nView option: ")
                viewOptions(option)
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