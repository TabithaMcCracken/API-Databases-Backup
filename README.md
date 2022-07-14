# API Backup

This is a Python based application to backup the Coding Nomads User and User Tasks data to a local SQL database. 
The goal of this project is to 

## Requirements

- Python 3.9
- MySQL

## Installation

Create a new schema called `taskdb` then install requirements and run the DB setup script.

```shell
python3 -m pip install -r requirements.txt
python3 DB_Setup.py
```

## Usage

```shell
python3 API_Database_Backup.py
```

## Tests

Go the extra mile and write tests for your application. Then provide examples on how to run them here.