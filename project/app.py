import mysql.connector as mariadb

# todo: create sql set up file that creates user 
# establish connection to mariadb database
db = mariadb.connect(
    host='localhost', 
    user='user1', 
    password='12345678', 
    database="task_db"
)

cursor = db.cursor()

# create database and tables

# cursor.execute("SHOW DATABASES")

# for x in cursor:
#     print(x)

cursor.execute("INSERT INTO task (taskno, task_title, date_created, deadline, task_description) VALUES (1, 'CMSC 127 Project SQL', '2022-05-02 17:00:00', '2022-05-11 23:59:59', 'Create an SQL file containing all your table definitions.'), (2, 'CMSC 127 Project Application', '2022-04-18 08:00:00', '2022-06-03 08:00:00', 'A task record system where you can list tasks and provide groupings and deadlines.')")
for x in cursor:
    print(x)

def app_loop(choice):
    while choice != 0:
        match choice:
            case '1':
                print("Adding task!")
            case '2':
                print("Editing task!")
            case '3':
                print("Deleting task!")
            case '4':
                print("Adding task!")
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
        choice = input("Choice: ")

print('------TO-DO APP------', '[1] Add/Create Task', '[2] Edit Task', '[3] Delete Task', '[4] View All Tasks', '[5] Mark Task as done', '[6] Add Category', '[7] Edit Category', '[8] Delete Category', '[9] View Category', '[10] Add a Task to a Category', '[11] View Task (per day, month)', '[0] Exit', sep='\n')
choice = input("Choice: ")
app_loop(choice)


