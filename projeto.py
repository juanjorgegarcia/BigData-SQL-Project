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
        cursor.execute('INSERT INTO person_favorites_bird (person_id, bird_name) VALUES (%s, %s)',
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


def find_post_id(conn, post_name):
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT post_id FROM post WHERE title = %s', (post_name))
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


def remove_post(conn, post_id):
    with conn.cursor() as cursor:
        cursor.execute(
            ' Update post SET post.deletedAt =  CURDATE() WHERE post_id=%s', (post_id))


def update_post_title(conn, post_id, value):
    with conn.cursor() as cursor:
        try:
            cursor.execute(
                'UPDATE post SET title=%s where post_id=%s', (value, post_id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso alterar a propriedade title do id {post_id} para {value} na tabela post')


def update_post_content(conn, post_id, value):
    with conn.cursor() as cursor:
        try:
            cursor.execute(
                'UPDATE post SET content=%s where post_id=%s', (value, post_id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso alterar a propriedade content do id {post_id} para {value} na tabela post')


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


def add_view(conn, person_id, post_id, ip, device, browser):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO person_view_post (person_id, post_id, ip, device, browser) VALUES (%s,%s,%s,%s,%s)',
                           (person_id, post_id, ip, device, browser))
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso inserir {person_id, post_id, ip, device, browser} na tabela view')


def find_view(conn, person_id, post_id):
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT person_id, post_id FROM person_view_post WHERE post_id = %s AND person_id=%s', (post_id, person_id))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None


def add_post_refere_person(conn, post_id, person_id):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post_refere_person (post_id, person_id) VALUES (%s,%s)',
                           (post_id, person_id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso inserir {post_id, person_id} na tabela post_refere_person')


def remove_post_refere_person(conn, post_id, person_id):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE post_refere_person SET deletedAt = CURDATE(), WHERE post_id = %s and person_id = %s ',
                           (post_id, person_id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso remover a referencia: {post_id, person_id} na tabela post_refere_person')


def list_all_references_person(conn, post_id, person_id):
    with conn.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM post_refere_person WHERE deletedAt is NULL and person_id = %s ',
                           (person_id))
            res = cursor.fetchall()
            return res
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso listar todas as referencias da pessoa: {person_id} na tabela post_refere_person')


def list_all_references_post(conn, post_id):
    with conn.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM post_refere_person WHERE deletedAt is NULL and post_id = %s ',
                           (post_id))
            res = cursor.fetchall()
            return res
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso listar todas as referencias do post: {post_id} na tabela post_refere_person')


def add_person_comment_post(conn, post_id, person_id, comment):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO person_comment_post (post_id ,person_id, comment) VALUES (%s,%s,%s)',
                           (post_id, person_id, comment))
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso inserir {post_id, person_id, comment} na tabela person_comment_person')


def remove_person_comment_post(conn, post_id, person_id):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE person_comment_post SET deletedAt = CURDATE(), WHERE post_id = %s and person_id = %s ',
                           (post_id, person_id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso remover o comentario: {post_id, person_id} na tabela person_comment_post')


def list_all_comments_of_person(conn, person_id):
    with conn.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM person_comment_post WHERE deletedAt is NULL and person_id = %s ',
                           (person_id))
            res = cursor.fetchall()
            return res
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso listar todas os comentarios da pessoa: {person_id} na tabela person_comment_post')


def list_all_comments_of_post(conn, post_id):
    with conn.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM person_comment_post WHERE deletedAt is NULL and post_id = %s ',
                           (post_id))
            res = cursor.fetchall()
            return res

        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso listar todas os comentarios do post: {post_id} na tabela person_comment_post')


def add_post_refere_bird(conn, post_id, bird_name):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post_refere_bird (post_id, bird_name) VALUES (%s,%s)',
                           (post_id, bird_name))
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso inserir {post_id, bird_name} na tabela post_refere_bird')


def remove_post_refere_bird(conn, post_id, bird_name):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE post_refere_bird SET deletedAt = CURDATE() WHERE post_id = %s and bird_name = %s ',
                           (post_id, bird_name))
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso remover a referencia: {post_id, bird_name} na tabela post_refere_bird')


def list_all_references_of_bird(conn, bird_name):
    with conn.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM post_refere_bird WHERE deletedAt is NULL and bird_name = %s ',
                           (bird_name))
            res = cursor.fetchall()
            return res
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso listar todas as referencias do passaro: {bird_name} na tabela post_refere_bird')


def list_all_bird_references_of_post(conn, post_id):
    with conn.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM post_refere_bird WHERE deletedAt is NULL and post_id = %s ',
                           (post_id))
            res = cursor.fetchall()
            return res
        except pymysql.err.IntegrityError as e:
            raise ValueError(
                f'Não posso listar todas os passaros do post: {post_id} na tabela post_refere_bird')
####

#  Parser

####


def parser(character, text):
    # return re.findall(r'\b[sS]\w+', text)
    return [idx for idx in text.split() if idx.lower().startswith(character.lower())]


def parse_and_refere(conn, content, post_id):
    users_refered = parser("@", content)
    birds_refered = parser("#", content)
    for u in users_refered:
        _id = find_person(conn, u)
        add_post_refere_person(conn, post_id, _id)
        print(u[1:])

    for b in birds_refered:
        add_post_refere_bird(conn, post_id, b)
        print(b[1:])
