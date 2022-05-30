------------------------------------------------------------
--  CMSC 127 ST-2L
--  Project: Task Record System
--  Milestone 03: SQL Queries

--  Members:
--  Cantero, Marco Jose
--  Macayan, Kyla Julienne
--  Ratuiste, Alesundreau Dale
--  Sotto, Francis Jay
------------------------------------------------------------

--  ddl
--  Table Definitions:
CREATE TABLE task(
    taskno INT AUTO_INCREMENT,
    task_title VARCHAR(50),
    date_created DATE,
    deadline DATE,
    date_completed DATE,
    task_description VARCHAR(100),
    task_status BOOLEAN,
    CONSTRAINT task_taskno_pk PRIMARY KEY(taskno)
    );
CREATE TABLE category(
    categoryno INT AUTO_INCREMENT,
    categoryname VARCHAR(50),
    categorycolor VARCHAR(20),
    CONSTRAINT category_categoryno_pk PRIMARY KEY(categoryno)
    );
CREATE TABLE belongsto(
    taskno INT(3),
    categoryno INT(3),
    CONSTRAINT belongsto_tasknocategoryno_pk PRIMARY KEY(taskno, categoryno),
    CONSTRAINT fk_taskno FOREIGN KEY(taskno) REFERENCES task(taskno),
    CONSTRAINT fk_categoryno FOREIGN KEY(categoryno) REFERENCES category(categoryno)
    );

--  dml
--  Sample SQL Queries for features: 
--  add/create task
INSERT INTO task (taskno, task_title, date_created, deadline, task_description) VALUES 
    (1, "CMSC 127 Project SQL", "2022-05-02 17:00:00", "2022-05-11 23:59:59", "Create an SQL file containing all your table definitions."), 
    (2, "CMSC 127 Project Application", "2022-04-18 08:00:00", "2022-06-03 08:00:00", "A task record system where you can list tasks and provide groupings and deadlines.");

--  edit task
UPDATE task SET task_description = "Create an SQL file containing all your table definitions. Also, include one sample query per project feature." WHERE taskno = 1;

--  delete task
DELETE FROM task WHERE taskno = 2;
DELETE FROM belongsto WHERE taskno = 3;     --di ako sure if eto ba talaga

--  view all tasks
SELECT task_title AS "Task", task_description AS "Description", deadline AS "Deadline", task_status AS "Status", categoryname AS "Category" FROM task LEFT JOIN category;

--  mark task as done
UPDATE task SET date_completed = "2022-05-11 12:00:00", task_status = 1 WHERE taskno = 1;

--  add category
INSERT INTO category VALUES
    (1, "Academic", "Green")
    (2, "Org-related", "Blue")
    (3, "Lovelife", "Red");

--  edit category
UPDATE category SET categoryname = "Money" WHERE categoryno = 1; 

--  delete category
DELETE FROM category WHERE categoryno = 3;
DELETE FROM belongsto WHERE categoryno = 3;     --di ako sure if eto ba talaga

--  view a category
SELECT * FROM category WHERE categoryno = 1;

--  add task to a category
INSERT INTO belongsto VALUES
    (1,1)
    (2,1);

--  view all tasks in a category
SELECT * FROM task WHERE taskno IN (SELECT taskno FROM belongsto WHERE categoryno = 1); 

--  view tasks per day
SELECT * FROM task WHERE DAY(deadline)=DAY(CURDATE());

--  view tasks per month
SELECT * FROM task WHERE MONTH(deadline)=MONTH(CURDATE());