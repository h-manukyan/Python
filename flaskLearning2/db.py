from ast import Dict
import pymysql
from pymysql.cursors import DictCursor

conn = pymysql.connect(
    host='sql7.freesqldatabase.com',
    database='sql7764026',
    user='sql7764026',
    password='tyFaTnW8tz',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

sql_query = """ CREATE TABLE IF NOT EXISTS book (
    id integer PRIMARY KEY,
    author text NOT NULL,
    language text NOT NULL,
    title text NOT NULL
)"""
cursor.execute(sql_query)
conn.close()
