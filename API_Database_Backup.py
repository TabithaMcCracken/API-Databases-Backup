# Backup user and task data from an API to my local database

# We Need To:
# Connect with the local database
# Get users data from the API
# Get data already in the 'users' table of the database
# Compare data, create new list with new data
# Add new data to the database
# Repeat for tasks


from pprint import pprint
from unittest import result
import sqlalchemy
from secret import password
import requests
import json
import pymysql

# Connect to local database
engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/taskDB')
connection = engine.connect()
metadata = sqlalchemy.MetaData()    

# User Backup

# Get user data from the API
def get_users_from_api(): # Function to get user data from API
    user_url = "http://demo.codingnomads.co:8080/tasks_api/users" 
    user_request = requests.get(user_url) # Gets data
    return user_request.json()['data']

# Get user data already in the 'users' table database
def get_users_from_db():
    users_table = sqlalchemy.Table('users', metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.select([users_table])
    result_proxy = connection.execute(query)
    return result_proxy.fetchall()

# Create new id list by comparing api and db id's 
def create_new_user_list():
    # Make a list of user id's from the database
    db_id_list = []
    for item in db_user_data:
        db_id_list.append(item[0])

    # Compare user ids in api to db and add new id's to the list
    new_user_id_list = []
    for api_item in api_user_data:
        if api_item['id'] not in db_id_list:
            new_user_id_list.append(api_item['id'])

    # Make new list of new api data by comparing the "id" to the list of new user ids
    new_user_data = []
    for item in new_user_id_list:
        for dics in api_user_data:
            if dics.get("id") == item:
                new_user_data.append(dics)

    return new_user_data

# Put the new data into the 'users' table
def put_new_user_data_in_db():
    users = sqlalchemy.Table('users', metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.insert(users)
    result_proxy = connection.execute(query, new_user_data)

api_user_data = get_users_from_api()
db_user_data = get_users_from_db()
new_user_data = create_new_user_list()
put_new_user_data_in_db()
print(f"Here is the list of new user data to be added to the database:\n{new_user_data}")


# Task Backup

# Get task data from the API
def get_tasks_from_api():
    task_url = "http://demo.codingnomads.co:8080/tasks_api/tasks"
    task_request = requests.get(task_url)
    return task_request.json()['data']

# Get task data already in the 'tasks' table database
def get_tasks_from_db():
    tasks_table = sqlalchemy.Table('Tasks', metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.select([tasks_table])
    result_proxy = connection.execute(query)
    return result_proxy.fetchall()

# Create new updatedAt list by comparing api and db udpatedAt
def create_new_task_list():
    # Create list of new tasks (using the "updatedAt" field)
    db_updatedAt_list = []
    for item in db_task_data:

        db_updatedAt_list.append(item['updatedAt'])
    
    # Compare task updatedAt in api to db and add new updatedAt to the list
    new_updatedAt_list = []
    for api_item in api_task_data:

        if api_item['updatedAt'] not in db_updatedAt_list:

            new_updatedAt_list.append(api_item['updatedAt'])

    # Create list of new task data
    new_task_data = [] 
    for item in new_updatedAt_list:
        for dics in api_task_data:
            if dics.get("updatedAt") == item:
                new_task_data.append(dics)

    return new_task_data

# Put the new data into the 'tasks' table
def put_new_task_data_in_db():
    tasks = sqlalchemy.Table('Tasks', metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.insert(tasks)
    result_proxy = connection.execute(query, new_task_data)


api_task_data = get_tasks_from_api()
db_task_data = get_tasks_from_db()
new_task_data = create_new_task_list()
put_new_task_data_in_db()
print(f"Here is the list of new tasks added to the database:\n{new_task_data}")