from functools import partial
import io
import json
from fastapi import FastAPI
from projeto import *
import os
import os.path
import subprocess
import pymysql
from pydantic import BaseModel

app = FastAPI()

global config


def run_db_query(connection, query, args=None):
    with connection.cursor() as cursor:
        print('Executando query:')
        cursor.execute(query, args)
        for result in cursor:
            print(result)


connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='birdbook')

db = partial(run_db_query, connection)


# def setUp():
#     run_sql_script('make_birdbook.sql')
#     print("olaaa")


@app.get("/")
def read_root():
    # return db("INSERT INTO person (username, first_name, last_name, email, city) VALUES ('arthurolgaaa','arthur','olga','a@a.com','sp')")
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO person (username, first_name, last_name, email, city) VALUES ('arthurolgaaa','arthur','olga','a@a.com','sp')")
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso inserir na tabela person')


@app.get("/users")
def read_users():
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                "SELECT * FROM person")
            res = cursor.fetchall()
            return res
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso ler a tabela person')
            return "nope"


class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    city: str


# @app.post("/users")
# def create_users(user: User):
#     print("aaa")
#     return add_person(connection, user.username, user.first_name, user.last_name, user.email, user.city)

@app.post("/users")
def create_users(user: User):
    # return db("INSERT INTO person (username, first_name, last_name, email, city) VALUES ('arthurolgaaa','arthur','olga','a@a.com','sp')")
    with connection.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO person (username, first_name, last_name, email, city) VALUES (%s,%s,%s,%s,%s)',
                           (user.username, user.first_name, user.last_name, user.email, user.city))
            return "Inserido"
        except pymysql.err.IntegrityError as e:
            return "erro ao inserir "+str(user.username)
            raise ValueError(
                f'Não posso inserir na tabela person')
