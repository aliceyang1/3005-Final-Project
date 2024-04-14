# 3005-Final-Project

### Description

Name: Alice Yang
Student number: 101277355

This is a simple Python3 application that manages student records from a PostgreSQL database.

[Video Link](https://youtu.be/C8_IFWYZ4TU)
[Diagrams](https://www.figma.com/file/KKlYS2FntQk1456iUspFNc/3005-final-project-ERD?type=whiteboard&node-id=0%3A1&t=niXhJvng0ZpWnUBm-1)

### PostgreSQL Database setup

- Open pgAdmin 4
- Create a new database called `fitness_management_system_db` in pgAdmin 4

### Install Python dependencies

Install [psycopg 2](https://pypi.org/project/psycopg/)


### How to run

1. Update the connection setting variable values in the code to match your PostgreSQL database connection information.

2. Run the following command in the terminal:

```bash
python3 projectCode.py
```

3. NOTE: some possible errors in the DML file might be caused by the ID mismatch when using auto-increment, if that happens, update the ID values according to the values in your environment. Sorry for the inconvinence!!