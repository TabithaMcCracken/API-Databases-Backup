""" Backup user and task data from the Coding Nomads API to a local database

# Steps:
# Connect with the local database
# Get 'users' data from the API
# Get data already in the 'users' table of the database
# Compare data, create new list with new data
# Add new data to the database
# Repeat for tasks API and database
"""

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

def get_users_from_api():
    """Gets user data from the API

    Returns:
        list: user data from the API
    """

    user_url = "http://demo.codingnomads.co:8080/tasks_api/users" 
    user_request = requests.get(user_url) # Gets data
    return user_request.json()['data']

# Get user data already in the 'users' table in the database
def get_users_from_db(metadata, engine, connection):
    """Get user data already in the 'users' table in the database

    Args:
        metadata (class): keeps features of the database together
        engine (class): manages connection to the database
        connection (class): facilitates the connection to the database

    Returns:
        list: user data from 'users' table in the database
    """

    users_table = sqlalchemy.Table('users', metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.select([users_table])
    result_proxy = connection.execute(query)
    return result_proxy.fetchall()

def create_new_user_list(db_user_data, api_user_data):
    """Creates new id list by comparing api and db id's

    Args:
        db_user_data (list): user data from db  
        api_user_data (list): user data from api

    Returns:
        list: list of new id's 
    """

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
def put_new_user_data_in_db(metadata, engine, connection, new_user_data):
    """Puts the new data based on new id's into the 'users' table of the db

    Args:
        metadata (class): keeps features of the database together
        engine (class): manages connection to the database
        connection (class): facilitates the connection to the database
    
    """
    if new_user_data:
        users = sqlalchemy.Table('users', metadata, autoload=True, autoload_with=engine)
        query = sqlalchemy.insert(users)
        result_proxy = connection.execute(query, new_user_data)
        print(f"Here is the list of new user data to be added to the database:\n{new_user_data}")

    else:
        print("The new user list is empty, no data was added to the database.")

api_user_data = get_users_from_api()
db_user_data = get_users_from_db(metadata, engine, connection)
new_user_data = create_new_user_list(db_user_data, api_user_data)
put_new_user_data_in_db(metadata, engine, connection, new_user_data)


# Task Backup

def get_tasks_from_api():
    """Gets tasks data from the api

    Returns:
        list: tasks data from the api
    """

    task_url = "http://demo.codingnomads.co:8080/tasks_api/tasks"
    task_request = requests.get(task_url)
    return task_request.json()['data']


def get_tasks_from_db(metadata, engine, connection):
    """Gets task data already in the 'tasks' table of the db

    Args:
        metadata (class): keeps features of the database together
        engine (class): manages connection to the database
        connection (class): facilitates the connection to the database

    Returns:
        list: task data from the db
    """

    tasks_table = sqlalchemy.Table('Tasks', metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.select([tasks_table])
    result_proxy = connection.execute(query)
    return result_proxy.fetchall()

def create_new_task_list(db_task_data, api_task_data):
    """Creates list of new tasks on the api by comparing api and db 'updatedAt' fields

    Args:
        db_task_data (list): task data from the db
        api_task_data (list): task data from the api

    Returns:
        list: new tasks on the api
    """

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

def put_new_task_data_in_db(metadata, engine, connection, new_task_data):
    """Puts the new tasks into the 'tasks' table in the db

    Args:
        metadata (class): keeps features of the database together
        engine (class): manages connection to the database
        connection (class): facilitates the connection to the database

    """

    if new_task_data:
        tasks = sqlalchemy.Table('tasks', metadata, autoload=True, autoload_with=engine)
        query = sqlalchemy.insert(tasks)
        result_proxy = connection.execute(query, new_task_data)
        print(f"Here is the list of new tasks added to the database:\n{new_task_data}")

    else:
        print("The new task list is empty, no data was added to the database.")


api_task_data = get_tasks_from_api()
db_task_data = get_tasks_from_db(metadata, engine, connection)
new_task_data = create_new_task_list(db_task_data, api_task_data)
put_new_task_data_in_db(metadata, engine, connection, new_task_data)
