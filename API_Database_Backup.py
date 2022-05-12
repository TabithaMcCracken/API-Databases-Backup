# Backup user and task data from an API to my local database

# We Need To:
# Get users data from the API
# Get data already in the 'users' table of the database
# Compare data, create new list with new data
# Add new data to the database
# Repeat for tasks


from pprint import pprint
import sqlalchemy
from secret import password
import requests
import json
import pymysql

engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/taskDB')
connection = engine.connect()
metadata = sqlalchemy.MetaData()    


# # Get user data from the API

# def get_users(): # Function to get user data from API
#     base_url = "http://demo.codingnomads.co:8080/tasks_api/users" 
#     request = requests.get(base_url) # Gets data
#     data = request.text # Data is a string
#     parsed_json = json.loads(data) # Converts data from json into a parsed json dict
#     return parsed_json

# parsed_user_data = get_users() # Call function to get our parsed user data from the API

# api_user_list = [] # Empty list for data to add only the data that we want
# def make_user_list(): # Function for accesssing and appending 'data'
#     user_data = parsed_user_data['data'] # accessing only the 'data' dict
#     for data in user_data: # going through all the data in the 'data' dict
#         api_user_list.append(data) # Appending data to a list

# make_user_list() # Call the function


# # Get data already in the 'users' table database

# users_table = sqlalchemy.Table('users', metadata, autoload=True, autoload_with=engine)
# query = sqlalchemy.select([users_table])
# result_proxy = connection.execute(query)
# db_users_list = result_proxy.fetchall() # Fetching all data from the 'users' table
# # pprint(db_users_list)

# # Compare data

# # Make a list of user id's from the database
# db_id_list = []
# for item in db_users_list:
#     db_id_list.append(item[0])

# # Compare user ids in api_user_list to db_users_list
# # Create list of new user id's
# new_user_id_list = []
# for api_item in api_user_list:
#     # print(api_item['id'])
#     if api_item['id'] not in db_id_list:
#         new_user_id_list.append(api_item['id'])
# print(new_user_id_list)

# # Make new list of just new api data by comparing the "id" to the list of new user ids
# new_user_list = []

# for item in new_user_id_list:
#     for dics in api_user_list:
#         if dics.get("id") == item:
#             new_user_list.append(dics)

# print(new_user_list)


# # Put the API data into the 'users' table
# users = sqlalchemy.Table('users', metadata, autoload=True, autoload_with=engine)
# query = sqlalchemy.insert(users)
# result_proxy = connection.execute(query, new_user_list)


# Task Backup

# Get task data from the API

def get_tasks(): # Function to get task data from API
    task_url = "http://demo.codingnomads.co:8080/tasks_api/tasks"
    task_request = requests.get(task_url)
    data = task_request.text
    parsed_json = json.loads(data)
    return parsed_json


parsed_api_task_data = get_tasks()
# pprint(parsed_api_task_data)

api_task_list = [] # Empty list for data to add only the data that we want
def make_task_list(): # Function for accesssing and appending 'data'
    task_data = parsed_api_task_data['data'] # accessing only the 'data' dict
    for data in task_data: # going through all the data in the 'data' dict
        api_task_list.append(data) # Appending data to a list

make_task_list() # Call the function
pprint(api_task_list)

# Get data already in the 'tasks' table database

tasks_table = sqlalchemy.Table('tasks', metadata, autoload=True, autoload_with=engine)
query = sqlalchemy.select([tasks_table])
result_proxy = connection.execute(query)
db_tasks_list = result_proxy.fetchall() # Fetching all data from the 'tasks' table
print(db_tasks_list)

# Compare data

# Make a list of task descriptions from the database
db_updatedAt_list = []
for item in db_tasks_list:
    db_updatedAt_list.append(item['updatedAt'])

# Compare user tasks  to db_users_list

# Create list of new tasks (using the "updatedAt" field)
new_updatedAt_list = []
for api_item in api_task_list:
    if api_item['updatedAt'] not in db_updatedAt_list:
        new_updatedAt_list.append(api_item['updatedAt'])
# print(new_updatedAt_list)

# # Make new list of just new api data by comparing the "id" to the list of new user ids
new_task_list = []

for item in new_updatedAt_list:
    for dics in api_task_list:
        if dics.get("updatedAt") == item:
            new_task_list.append(dics)

# print(new_task_list)

# Put the API data into the 'users' table
tasks = sqlalchemy.Table('tasks', metadata, autoload=True, autoload_with=engine)
query = sqlalchemy.insert(tasks)
result_proxy = connection.execute(query, new_task_list)

