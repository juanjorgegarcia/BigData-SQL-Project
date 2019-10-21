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
def read_bird():
    try:
        return list_birds(conn)
    except:
        return f'Não posso listar todos os passaros'

@app.get("/bird/urls")
def read_bird():
    try:
        return list_birds(conn)
    except:
        return f'Não posso listar todos os passaros'



@app.post("/bird")
def create_bird(bird: Bird):
    try:
        add_bird(conn, bird.bird_name)
        conn.commit()
        return f"Passaro: {bird.bird_name} foi adicionado"
    except:
        return f'Não posso inserir o passaro {bird.bird_name}'


@app.delete("/bird")
def delete_bird(bird: Bird):
    try:
        b = find_bird(conn, bird.bird_name)
        if b:
            remove_bird(conn, bird.bird_name)
            conn.commit()
            return f"Passaro: {bird.bird_name} foi deletado"
        else:
            return f"Passaro: {bird.bird_name} nao existe"
    except:
        return f'Não posso remover o passaro: {bird.bird_name}'


@app.get("/post/comments")
def read_posts_comments(title: str):
    try:
        post_id = find_post_id(conn, title)

        if post_id:
            return list_all_comments_of_post(conn, post_id)
        else:
            return f"Nao existe um post com o titulo {title}"
    except:
        return f'Não posso listar todos os comentarios do post: {title}'


@app.post("/post/comment")
def create_post_comment(title: str, username: str, comment: str):
    try:
        post_id = find_post_id(conn, title)
        person_id = find_person(conn, username)
        if person_id:
            if post_id:
                add_person_comment_post(conn, post_id, person_id, comment)
                conn.commit()
                return f"Post: {title} foi adicionado pelo usuario {username}"
            else:
                return f"Nao existe um post com o titulo {title}"
        else:
            return f"Nao existe uma pessoa com o username {username}"

    except:
        return f'Não posso inserir o comentario {comment} do usuario: {username} no post: {title}'


@app.delete("/post/comment")
def delete_post_comment(title: str, username: str):
    try:
        post_id = find_post_id(conn, title)
        person_id = find_person(conn, username)
        if person_id:
            if post_id:
                remove_person_comment_post(conn, post_id, person_id)
                conn.commit()
                return f"Comentario no post: {title} foi removido pelo usuario {username}"
            else:
                return f"Nao existe um post com o titulo {title}"
        else:
            return f"Nao existe uma pessoa com o username {username}"
    except:
        return f'Não posso remover o comentario do post com o titulo: {title}'


@app.put("/post/comment")
def update_post_comment(title: str, username: str, comment: str):
    try:
        post_id = find_post_id(conn, title)
        person_id = find_person(conn, username)
        if person_id:
            if post_id:
                update_person_comment_post(conn, post_id, person_id, comment)
                conn.commit()
                return f"Comentario do usuario: {username} no post: {title} foi atualiado para usuario {comment}"
            else:
                return f"Nao existe um post com o titulo {title}"
        else:
            return f"Nao existe uma pessoa com o username {username}"
    except:
        return f'Não posso atualizar o comentario do post com o titulo: {title}'


@app.get("/post/votes")
def read_posts_votes(title: str):
    try:
        post_id = find_post_id(conn, title)
        if post_id:
            return list_all_votes_of_post(conn, post_id)
        else:
            return f"Nao existe um post com o titulo {title}"
    except:
        return f'Não posso listar todos os votos do post: {title}'


@app.post("/post/vote")
def create_post_vote(title: str, username: str, like: int):
    try:
        post_id = find_post_id(conn, title)
        person_id = find_person(conn, username)
        if person_id:
            if post_id:
                add_person_vote_post(conn, post_id, person_id, like)
                conn.commit()
                return f"Vote: {like} no Post: {title} foi adicionado pelo usuario {username}"
            else:
                return f"Nao existe um post com o titulo {title}"
        else:
            return f"Nao existe uma pessoa com o username {username}"

    except:
        return f'Não posso inserir o vote: {like} do usuario: {username} no post: {title}'


@app.delete("/post/vote")
def delete_post_vote(title: str, username: str):
    try:
        post_id = find_post_id(conn, title)
        person_id = find_person(conn, username)
        if person_id:
            if post_id:
                remove_person_vote_post(conn, post_id, person_id)
                conn.commit()
                return f"Vote no post: {title} foi removido pelo usuario {username}"
            else:
                return f"Nao existe um post com o titulo {title}"
        else:
            return f"Nao existe uma pessoa com o username {username}"
    except:
        return f'Não posso remover o comentario do post com o titulo: {title}'


@app.put("/post/vote")
def update_post_vote(title: str, username: str, like: str):
    try:
        post_id = find_post_id(conn, title)
        person_id = find_person(conn, username)
        if person_id:
            if post_id:
                update_person_vote_post(conn, post_id, person_id, like)
                conn.commit()
                return f"Vote do usuario: {username} no post: {title} foi atualizado para vote: {like}"
            else:
                return f"Nao existe um post com o titulo {title}"
        else:
            return f"Nao existe uma pessoa com o username {username}"
    except:
        return f'Não posso atualizar o comentario do post com o titulo: {title}'


@app.get("/user/comments")
def read_posts_comments(username: str):
    try:
        person_id = find_person(conn, username)
        if person_id:
            return list_all_comments_of_person(conn, person_id)
        else:
            return f"Nao existe um usuario com o username {username}"
    except:
        return f'Não posso listar todos os comentarios do usuario: {username}'


@app.get("/user/posts")
def read_user_posts(username: str):
    try:
        person_id = find_person(conn, username)
        if person_id:
            return list_active_posts_of_person(conn, person_id)
        else:
            return f"Nao existe um usuario com o username {username}"
    except:
        return f'Não posso listar todos os posts do usuario: {username}'


@app.get("/user/birds")
def read_user_birds(username: str):
    try:
        person_id = find_person(conn, username)
        if person_id:
            return list_birds_of_person(conn, person_id)
        else:
            return f"Nao existe um usuario com o username {username}"
    except:
        return f'Não posso listar todos os passaros do usuario: {username}'


@app.post("/user/birds")
def add_user_bird(username: str, bird_name: str):
    try:
        person_id = find_person(conn, username)
        bird = find_bird(conn, bird_name)
        if person_id:
            if bird:
                add_bird_to_person(conn, person_id, bird_name)
                conn.commit()

                return f"Passaro: {bird} adicionado ao usuario {username}"
            else:
                return f"Nao existe um passaro com o {bird_name}"
        else:
            return f"Nao existe um usuario com o username {username}"
    except:
        return f'Não posso adicionar o passaro: {bird_name} ao usuario: {username}'


@app.get("/user/votes")
def read_user_birds(username: str):
    try:
        person_id = find_person(conn, username)
        if person_id:
            return list_all_votes_of_person(conn, person_id)
        else:
            return f"Nao existe um usuario com o username {username}"
    except:
        return f'Não posso listar todos os votes do usuario: {username}'


@app.get("/popular/users/city")
def read_popular_users_city():
    try:

        return list_popular_users_city(conn)
    except:
        return f'Não posso listar os usuarios mais populares de cada cidade '


@app.get("/post/views")
def read_posts_views(title: str):
    try:
        post_id = find_post_id(conn, title)
        if post_id:
            return list_post_views(conn, post_id)
        else:
            return f"Nao existe um post com o titulo {title}"
    except:
        return f'Não posso listar todos os views do post: {title}'


@app.post("/post/view")
def create_post_view(title: str, username: str, ip: str, browser: str):
    try:
        post_id = find_post_id(conn, title)
        person_id = find_person(conn, username)
        if person_id:
            if post_id:
                add_view(conn, post_id, post_id, ip, device, browser)
                conn.commit()
                return f"Post: {title} foi visto pelo usuario {username}"
            else:
                return f"Nao existe um post com o titulo {title}"
        else:
            return f"Nao existe uma pessoa com o username {username}"

    except:
        return f'Não posso inserir o comentario {comment} do usuario: {username} no post: {title}'


@app.delete("/post/view")
def delete_post_view(title: str, username: str):
    try:
        post_id = find_post_id(conn, title)
        person_id = find_person(conn, username)
        if person_id:
            if post_id:
                remove_view(conn, person_id, post_id)
                conn.commit()
                return f"View no post: {title} foi removido pelo usuario {username}"
            else:
                return f"Nao existe um post com o titulo {title}"
        else:
            return f"Nao existe uma pessoa com o username {username}"
    except:
        return f'Não posso remover o comentario do post com o titulo: {title}'


@app.get("/user/views")
def read_user_views(username: str):
    try:
        person_id = find_person(conn, username)
        if person_id:
            return list_users_views(conn, person_id)
        else:
            return f"Nao existe um usuario com o username {username}"
    except:
        return f'Não posso listar todos os views do usuario: {username}'


@app.get("/user/references")
def read_user_references(username: str):
    try:
        person_id = find_person(conn, username)
        if person_id:
            return list_user_references(conn, person_id)
        else:
            return f"Nao existe um usuario com o username {username}"
    except:
        return f'Não posso listar todos as marcacoes do usuario: {username}'


@app.get("/devices/top")
def read_user_references(username: str):
    try:
        return list_top_devices(conn)
    except:
        return f'Não posso listar todos os top devices: {username}'
