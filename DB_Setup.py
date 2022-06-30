'''

This script sets up 2 tables in a database to mirror the data in the Coding Nomads 
demo API. 
http://demo.codingnomads.co:8080/tasks_api/users
http://demo.codingnomads.co:8080/tasks_api/tasks

Change the database and password info for your database

'''
from secret import password
import sqlalchemy

engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/taskDB')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

# Create Users table
users_table = sqlalchemy.Table('Users', metadata, \
     sqlalchemy.Column('id', sqlalchemy.Integer(), nullable=False), \
     sqlalchemy.Column('email', sqlalchemy.String(100), nullable=True), \
     sqlalchemy.Column('first_name', sqlalchemy.String(100), nullable=True), \
     sqlalchemy.Column('last_name', sqlalchemy.String(100), nullable=True), \
     sqlalchemy.Column('created_at', sqlalchemy.BigInteger(), nullable=True), \
     sqlalchemy.Column('updated_at', sqlalchemy.BigInteger(), nullable=True)
     )

# Create Tasks table
tasks_table = sqlalchemy.Table('Tasks', metadata, \
    sqlalchemy.Column('id', sqlalchemy.Integer(), nullable=False), \
    sqlalchemy.Column('userId', sqlalchemy.Integer(), nullable=False), \
    sqlalchemy.Column('name', sqlalchemy.String(100), nullable=True), \
    sqlalchemy.Column('description', sqlalchemy.String(200), nullable=True), \
    sqlalchemy.Column('createdAt', sqlalchemy.BigInteger(), nullable=True), \
    sqlalchemy.Column('updatedAt', sqlalchemy.BigInteger(), nullable=True), \
    sqlalchemy.Column('completed', sqlalchemy.Boolean(), nullable=True)
    )
metadata.create_all(engine)


# SQL to create User table
# CREATE TABLE `taskDB`.`User_2` (
#   `id` INT NULL DEFAULT NULL,
#   `email` VARCHAR(100) NULL DEFAULT NULL,
#   `first_name` VARCHAR(100) NULL DEFAULT NULL,
#   `last_name` VARCHAR(100) NULL DEFAULT NULL,
#   `created_at` BIGINT NULL DEFAULT NULL,
#   `updated_at` BIGINT NULL DEFAULT NULL);