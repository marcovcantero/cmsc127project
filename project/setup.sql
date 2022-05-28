--  Table Definitions:
CREATE DATABASE task_db;
USE task_db;
CREATE TABLE task(
    taskno INT(3),
    title VARCHAR(50),
    date_created TIMESTAMP,
    deadline TIMESTAMP,
    date_completed TIMESTAMP,
    task_description VARCHAR(100),
    task_status BOOLEAN,
    CONSTRAINT task_taskno_pk PRIMARY KEY(taskno)
    );

CREATE TABLE category(
    categoryno INT(3),
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

--- create user to be used in python file and grant it all privileges to task_db
CREATE USER 'user1'@'localhost' IDENTIFIED BY '12345678';

GRANT ALL PRIVILEGES ON task_db.* TO user1;