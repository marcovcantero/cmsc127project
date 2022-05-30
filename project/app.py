import mysql.connector as mariadb

# establish connection to mariadb database
db = mariadb.connect(
    host='localhost', 
    user='user1', 
    password='12345678', 
    database="task_db"
)

cursor = db.cursor()

# create database and tables
def addTask(taskTitle, dateCreated, deadline, taskDescription):
    try:
        insertQuery = """INSERT INTO task (task_title, date_created, deadline, task_description) VALUES (%s, %s, %s, %s)"""
        data = (taskTitle, dateCreated, deadline, taskDescription)
        cursor.execute(insertQuery, data)
        db.commit()
        print("Added task successfully.")
        
    except mariadb.Error as e:
        print("Failed to add task. Error: {}".format(e))
        
def editTaskTitle(taskTitle, taskNo):
    try:
        updateQuery = """UPDATE task SET task_title = %s WHERE taskno = %s"""
        data = (taskTitle, taskNo)
        cursor.execute(updateQuery, data)
        db.commit()
        print("Edited task title successfully.")
        
    except mariadb.Error as e:
        print("Failed to edit task title. Error: {}".format(e))
        
def editDateCreated(dateCreated, taskNo):
    try:
        updateQuery = """UPDATE task SET date_created = %s WHERE taskno = %s"""
        data = (dateCreated, taskNo)
        cursor.execute(updateQuery, data)
        db.commit()
        print("Edited date created successfully.")
        
    except mariadb.Error as e:
        print("Failed to edit date created. Error: {}".format(e))
        
def editDeadline(deadline, taskNo):
    try:
        updateQuery = """UPDATE task SET deadline = %s WHERE taskno = %s"""
        data = (deadline, taskNo)
        cursor.execute(updateQuery, data)
        db.commit()
        print("Edited deadline successfully.")
        
    except mariadb.Error as e:
        print("Failed to edit deadline. Error: {}".format(e))
        
def editDateCompleted(dateCompleted, taskNo):
    try:
        updateQuery = """UPDATE task SET date_completed = %s WHERE taskno = %s"""
        data = (dateCompleted, taskNo)
        cursor.execute(updateQuery, data)
        db.commit()
        print("Edited date completed successfully.")
        
    except mariadb.Error as e:
        print("Failed to edit date completed. Error: {}".format(e))
        
def editTaskDescription(taskDescription, taskNo):
    try:
        updateQuery = """UPDATE task SET task_description = %s WHERE taskno = %s"""
        data = (taskDescription, taskNo)
        cursor.execute(updateQuery, data)
        db.commit()
        print("Edited task description successfully.")
        
    except mariadb.Error as e:
        print("Failed to edit task description. Error: {}".format(e))
        
def deleteTask(taskNo):
    try:
        deleteQuery = """DELETE FROM task WHERE taskno = %s"""
        cursor.execute(deleteQuery, (taskNo,))
        db.commit()
        print("Deleted task successfully.")
        
    except mariadb.Error as e:
        print("Failed to delete task. Error: {}".format(e))
        
def viewAllTask():
    try:
        selectQuery = """SELECT * FROM task"""
        cursor.execute(selectQuery)
        data = cursor.fetchall()
        print("\nTotal number of tasks: ", cursor.rowcount)
        print("\nTo-Do List")
        for row in data:
            print("\nTask No. ", row[0])
            print("Task Title: ", row[1])
            print("Date Created: ", row[2])
            print("Deadline: ", row[3])
            print("Date Completed: ", row[4])
            print("Task Status: ", row[5])
    
    except mariadb.Error as e:
        print("Failed to view all tasks. Error: {}".format(e))

# cursor.execute("SHOW DATABASES")

# for x in cursor:
#     print(x)

#cursor.execute("INSERT INTO task (taskno, task_title, date_created, deadline, task_description) VALUES (1, 'CMSC 127 Project SQL', '2022-05-02 17:00:00', '2022-05-11 23:59:59', 'Create an SQL file containing all your table definitions.'), (2, 'CMSC 127 Project Application', '2022-04-18 08:00:00', '2022-06-03 08:00:00', 'A task record system where you can list tasks and provide groupings and deadlines.')")
#for x in cursor:
#    print(x)

def editOptions(option):
    while option != 0:
        match option:
            case '1':
                data1 = input("Enter new task title: ")
                data2 = input("Enter task number: ")
                editTaskTitle(data1, data2)
            case '2':
                data1 = input("Enter new date (yyyy-MM-dd): ")
                data2 = input("Enter task number: ")
                editDateCreated(data1, data2)
            case '3':
                data1 = input("Enter new deadline (yyyy-MM-dd): ")
                data2 = input("Enter task number: ")
                editDeadline(data1, data2)
            case '4':
                data1 = input("Enter new date (yyyy-MM-dd): ")
                data2 = input("Enter task number: ")
                editDateCompleted(data1, data2)
            case '5':
                data1 = input("Enter new task description: ")
                data2 = input("Enter task number: ")
                editTaskDescription(data1, data2)
            case '0':
                main()
            case _:
                print("Invalid input.")
        option = input("\nEdit option: ")

def app_loop(choice):
    while choice != 0:
        match choice:
            case '1':
                data1 = input("Enter task title: ")
                data2 = input("Enter date created (yyyy-MM-dd): ")
                data3 = input("Enter deadline (yyyy-MM-dd): ")
                data4 = input("Enter task description: ")
                addTask(data1, data2, data3, data4)
            case '2':
                print('\n------EDIT TASK------', '[1] Edit Task Title', '[2] Edit Date Created', '[3] Edit Deadline', '[4] Edit Date Completed', '[5] Edit Task Description', '[0] Back', sep='\n')
                option = input("\nEdit option: ")
                editOptions(option)
            case '3':
                taskNo = input("Enter task number: ")
                deleteTask(taskNo)
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
                print("Exiting app!")
                quit()
            case _:
                print("Invalid input.")
        choice = input("\nChoice: ")
        
def main():
    print('\n------TO-DO APP------', '[1] Add/Create Task', '[2] Edit Task', '[3] Delete Task', '[4] View All Tasks', '[5] Mark Task as done', '[6] Add Category', '[7] Edit Category', '[8] Delete Category', '[9] View Category', '[10] Add a Task to a Category', '[11] View Task (per day, month)', '[0] Exit', sep='\n')
    choice = input("\nChoice: ")
    app_loop(choice)

main()


