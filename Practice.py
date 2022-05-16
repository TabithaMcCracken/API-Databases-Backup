from pprint import pprint
import sqlalchemy
from secret import password
import requests
import json
import pymysql








def get_tasks_from_api(): # Function to get task data from API
    task_url = "http://demo.codingnomads.co:8080/tasks_api/tasks"
    task_request = requests.get(task_url)
    return task_request.json()['data']

api_task_data = get_tasks_from_api()
pprint(api_task_data)