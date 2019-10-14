import pymysql


def add_person(conn, username, first_name, last_name, email, city):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO person (username, first_name, last_name, email, city) VALUES (%s,%s,%s,%s,%s)',
                           (username, first_name, last_name, email, city))
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso inserir {username, first_name, last_name, email, city} na tabela person')


def find_person(conn, username):
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT person_id FROM person WHERE username = %s', (username))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None


def update_person_username(conn, person_id, value):
    with conn.cursor() as cursor:
        try:
            cursor.execute(
                'UPDATE person SET username=%s where person_id=%s', (value, person_id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso alterar a propriedade username do id {person_id} para {value} na tabela person')


def remove_person(conn, person_id):
    with conn.cursor() as cursor:
        cursor.execute(
            'update person SET is_deleted = 1 where person_id=%s', (person_id))


def list_persons(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT person_id from person WHERE is_deleted =0')
        res = cursor.fetchall()
        persons = tuple(x[0] for x in res)
        return persons


def add_bird(conn, name):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO bird (bird_name) VALUES (%s)', (name))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {name} na tabela bird')


def find_bird(conn, name):
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT bird_name FROM bird WHERE bird_name = %s', (name))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None


def remove_bird(conn, bird_name):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM bird WHERE bird_name=%s', (bird_name))


def list_birds(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT bird_name from bird')
        res = cursor.fetchall()
        bird = tuple(x[0] for x in res)
        return bird


def add_bird_to_person(conn, person_id, bird_name):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO person_favorites_bird VALUES (%s, %s)',
                       (person_id, bird_name))


def delete_bird_of_person(conn, person_id, bird_name):
    with conn.cursor() as cursor:
        cursor.execute(
            'DELETE FROM person_favorites_bird WHERE person_id=%s AND bird_name=%s', (person_id, bird_name))


def lists_birds_of_person(conn, person_id):
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT bird_name FROM person_favorites_bird WHERE person_id=%s', (person_id))
        res = cursor.fetchall()
        birds = tuple(x[0] for x in res)
        return birds


def lists_persons_of_bird(conn, bird_name):
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT person_id FROM person_favorites_bird WHERE bird_name=%s', (bird_name))
        res = cursor.fetchall()
        persons = tuple(x[0] for x in res)
        return persons


def add_post(conn, title, url, content, person_id):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post (title, url, content, person_id) VALUES (%s,%s,%s,%s)',
                           (title, url, content, person_id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso inserir {title, url, content} na tabela post')


def find_post(conn, post_id):
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT post_id FROM post WHERE post_id = %s', (post_id))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None


def find_active_post(conn, post_id):
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT post_id FROM post WHERE post_id = %s AND deletedAt IS NULL', (post_id))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None


def update_post(conn, post_id, key, value):
    with conn.cursor() as cursor:
        try:
            cursor.execute(
                'UPDATE postn SET %s=%s where post_id=%s', (key, value, post_id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso alterar a propriedade {key} do id {post_id} para {value} na tabela post')


def remove_post(conn, post_id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM post WHERE post_id=%s', (post_id))


def delete_post_from_person(conn, person_id, post_id):
    with conn.cursor() as cursor:
        cursor.execute(
            'DELETE FROM person_make_post WHERE person_id=%s AND post_id=%s', (person_id, post_id))


def lists_posts_of_person(conn, person_id):
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT post_id FROM post WHERE person_id=%s', (person_id))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts


def lists_active_posts_of_person(conn, person_id):
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT post_id FROM post WHERE person_id=%s AND deletedAt IS NULL', (person_id))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts


def lists_persons_from_post(conn, post_id):
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT person_id FROM person_make_post WHERE post_id=%s', (post_id))
        res = cursor.fetchall()
        persons = tuple(x[0] for x in res)
        return persons
