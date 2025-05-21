import os

DB_HOST = os.getenv('MYSQL_HOST', 'db')
DB_USER = os.getenv('MYSQL_USER', 'admin')
DB_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD', 'admin')
DB_NAME = os.getenv('MYSQL_DATABASE', 'taskdb')
