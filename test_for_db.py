import sqlalchemy
from secret import password

engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/taskDB')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

new_task_data = {
    'id': 50,
    'userId': 190,
    'name': 'finish program',
    'description': 'get this program to work'
}

tasks = sqlalchemy.Table('Tasks', metadata, autoload=True, autoload_with=engine)
query = sqlalchemy.insert(tasks)
result_proxy = connection.execute(query, new_task_data)