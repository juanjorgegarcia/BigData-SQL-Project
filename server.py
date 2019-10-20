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
from projeto import *
app = FastAPI()

global config


def run_db_query(conn, query, args=None):
    with conn.cursor() as cursor:
        print('Executando query:')
        cursor.execute(query, args)
        for result in cursor:
            print(result)


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='birdbook')

db = partial(run_db_query, conn)


class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    city: str


class Post(BaseModel):
    title: str
    url: str
    content: str
    username: str


class Bird(BaseModel):
    bird_name: str


@app.get("/user")
def read_users():
    try:
        return list_persons(conn)
    except:
        return f'Não posso listar as pessoas na tabela person'


@app.post("/user")
def create_user(user: User):
    try:
        add_person(conn, user.username, user.first_name,
                   user.last_name, user.email, user.city)
        conn.commit()
        return "Pessoa foi adicionada"
    except:
        return f'Não posso inserir {user.username, user.first_name, user.last_name, user.email, user.city} na tabela person'


@app.delete("/user")
def delete_user(username: str):
    try:
        person_id = find_person(conn, username)
        if person_id:
            remove_person(conn, person_id)
            conn.commit()
            return f"Pessoa: {username} foi removida"
        else:
            return f"Nao existe uma pessoa com o username {username}"

    except:
        return f'Não posso remover a pessoa com o username: {username} na tabela person'


@app.put("/user")
def update_user_username(username: str, new_username: str):
    try:
        person_id = find_person(conn, username)
        if person_id:
            update_person_username(conn, person_id, new_username)
            conn.commit()
            return f"Username alterado de: {username} para: {new_username}"
        else:
            return f"Nao existe uma pessoa com o username {username}"
    except:
        return f'Não posso alterar o username para: {new_username} tente outro username'


@app.get("/post")
def read_posts():
    try:
        return list_posts(conn)
    except:
        return f'Não posso listar todos os posts'


@app.post("/post")
def create_post(post: Post):

    try:
        person_id = find_person(conn, post.username)
        if person_id:
            add_post(conn, post.title, post.url, post.content, person_id)
            conn.commit()
            return f"Post: {post.title} foi adicionado pelo usuario {post.username}"
        else:
            return f"Nao existe uma pessoa com o usernmae {post.username}"

    except:
        return f'Não posso inserir o post {post.title, post.url, post.content} do usuario: {post.username}'


@app.delete("/post")
def delete_post(title: str):
    try:
        post_id = find_post_id(conn, title)
        if post_id:
            remove_post(conn, post_id)
            conn.commit()
            return f"Post: {title} foi removido"
        else:
            return f"Nao existe um post com o titulo {title}"
    except:
        return f'Não posso remover o post com o titulo: {title}'


@app.put("/post")
def update_post(title: str, content: str):
    try:
        post_id = find_post_id(conn, title)
        if post_id:
            update_post_content(conn, post_id, content)
            conn.commit()
            return f"Conteudo do post: {title} alterado para: {content}"
        else:
            return f"Nao existe um post com o titulo {title}"
    except:
        return f'Não posso alterar o conteudo do post: {title} para: {content}'


@app.get("/bird")
def read_posts():
    try:
        return list_birds()
    except:
        return f'Não posso listar todos os passaros'


@app.post("/bird")
def create_bird(bird: Bird):

    try:
        add_bird(conn, bird_name)
        return f"Passaro: {bird.bird_name} foi adicionado"

    except:
        return f'Não posso inserir o passaro {bird.birdname}'


@app.delete("/bird")
def delete_post(bird: Bird):
    try:
        remove_bird(conn, bird.bird_name)
        return f"Passaro: {bird.bird_name} foi deletado"
    except:
        return f'Não posso remover o passaro: {bird.bird_name}'
