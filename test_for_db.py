# A few tests to run on API_Database_Backup

import sqlalchemy
from secret import password
import requests
import json

# Adds new data to the taskDB
engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/taskDB')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

def add_task_data_to_db():
    new_task_data = {
        'id': 50,
        'userId': 190,
        'name': 'finish program',
        'description': 'get this program to work'
    }

    tasks = sqlalchemy.Table('Tasks', metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.insert(tasks)
    result_proxy = connection.execute(query, new_task_data)

# add_task_data_to_db()

# Adds new data to the tasks api
def create_task_in_api():
    task_url = "http://demo.codingnomads.co:8080/tasks_api/tasks"
    userId_input = input("Please enter your user id: \n")
    task_name = input("Please enter your task: \n")
    task_des = input("Please enter a description of your task: \n")
    user_flag = input("Is your task already completed? Yes or No\n")
    completed_flag = False
    if user_flag == "Yes":
        completed_flag = True

    body = {
        "userId": userId_input,
        "name": task_name,
        "description": task_des,
        "completed": completed_flag
    }

    task_post = requests.post(task_url, json=body)
    print(task_post.status_code)
    
    if task_post.status_code == 200 or task_post.status_code == 201:
        print("Congratulations you have created a new task!")

create_task_in_api()