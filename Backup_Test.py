from pprint import pprint
import requests
import json


def get_tasks():
    task_url = "http://demo.codingnomads.co:8080/tasks_api/tasks"
    task_request = requests.get(task_url)
    data = task_request.text
    parsed_json = json.loads(data)
    return parsed_json

# Create a new user
def create_new_user():
    user_url = "http://demo.codingnomads.co:8080/tasks_api/users"

    first_name = input("What is your first name?")
    last_name = input("What is your last name?")
    email = input("What is your email address?")

    body = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email
    }

    account_post = requests.post(user_url, json=body)
    
    if account_post.status_code == 200 or account_post.status_code == 201:
        print("Congratulations you have created a new account!")
        response = requests.get(user_url)
        data = response.json()
        new_data = data["data"][-1]["id"]
        print(f"Your user id is: \n{new_data}")

# Create a new task
def create_task():
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
    
    if task_post.status_code == 200 or task_post.status_code == 201:
        print("Congratulations you have created a new task!")

# Update a tasks comletion status
def update_task():
    # Get task data
    task_data = get_tasks()
    # Get only "data"
    user_data = task_data["data"]

    id = int()
    description = str()
    userId_input = int(input("Please enter your user Id: \n"))

    task_list = []
    
    for task_data in user_data:
        task_access = task_data["userId"]
        if task_access == userId_input:
            task = task_data["name"]
            task_list.append(task)
            
    print(f"Here is your task list: \n {task_list}")
    
    update_task = input("Which task would you like to update to complete?")
    user_flag = input("Is your task already completed? Yes or No\n")
    completed_flag = False # Defaults to not completed
    if user_flag == "Yes":
        completed_flag = True
    elif user_flag == "No":
        completed_flag = False

    # Get id based on userId and name

    for task in user_data:
        task_access = task["userId"]
        task_name = task["name"]
        if task_access == userId_input and task_name == update_task:
            id = task["id"]
            description = task["description"]

    body = {
        "id": id,
        "userId": userId_input,
        "name": update_task,
        "description": description,
        "completed": completed_flag
    }
    task_url = "http://demo.codingnomads.co:8080/tasks_api/tasks"
    task_put = requests.put(task_url, json=body)
    print(task_put.status_code)
    if task_put.status_code == 200 or task_put.status_code == 201:
        print("You have updated a task!")


def which_task():
    task = int(input(
        "Please select from the following options (enter the number of the action "
        "you'd like to take):\n"
        "1) Create a new account (POST)\n"
        "2) Create a new task (POST)\n"
        "3) Update an existing task (PATCH/PUT)\n"
    ))
    print(f"You have selected option: {task}")

    if task == 1:
        create_new_user()
    elif task == 2:
        create_task()
    elif task == 3:
        update_task()


which_task()