import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql

from projeto import *


class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='birdbook'
        )

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION')

    def tearDown(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('ROLLBACK')

    def test_add_person(self):
        conn = self.__class__.connection

        username = 'juanjg'
        first_name = 'juan'
        last_name = 'jorge garcia'
        email = 'juanjg@al.insper.edu.br'
        city = 'sao jose do rio preto'

        # Adiciona um person não existente.
        add_person(conn, username, first_name, last_name, email, city)

        # Tenta adicionar o mesmo person duas vezes.
        try:
            add_person(conn,  username, first_name, last_name, email, city)
            self.fail('Nao deveria ter adicionado o mesmo person duas vezes.')
        except ValueError as e:
            pass

        # Checa se o person existe.
        person_id = find_person(conn, username)
        self.assertIsNotNone(person_id)

        # Tenta achar um person inexistente.
        person_id = find_person(conn, 'usernameqnaoexiste')
        self.assertIsNone(person_id)

    def test_remove_person(self):
        conn = self.__class__.connection

        username = 'juanjg'
        first_name = 'juan'
        last_name = 'jorge garcia'
        email = 'juanjg@al.insper.edu.br'
        city = 'sao jose do rio preto'

        add_person(conn, username, first_name, last_name, email, city)

        # Recebee o id da pessoa
        person_id = find_person(conn, username)

        res = list_persons(conn)
        self.assertCountEqual(res, (person_id,))
        # Remove a pessoa
        remove_person(conn, person_id)

        res = list_persons(conn)
        self.assertFalse(res)

    def test_muda_nome_person(self):
        conn = self.__class__.connection

        username = 'juanjg'
        first_name = 'juan'
        last_name = 'jorge garcia'
        email = 'juanjg@al.insper.edu.br'
        city = 'sao jose do rio preto'

        add_person(conn, username, first_name, last_name, email, city)

        username2 = 'arthurqmo'
        first_name2 = 'arthur'
        last_name2 = 'folga'
        email2 = 'arthurqmo@al.insper.edu.br'
        city2 = 'sao paulo'

        add_person(conn, username, first_name2, last_name2, email2, city2)
        person_id = find_person(conn, username2)

        # Tenta mudar nome para algum nome já existente.
        try:
            update_person(conn, person_id, 'username', 'juanjg')
            self.fail('Não deveria ter mudado o nome.')
        except ValueError as e:
            pass

        # Tenta mudar nome para nome inexistente.
        update_person(conn, person_id, 'username', 'jjautenticado')
        # Verifica se mudou.
        id_novo = find_person(conn, 'jjautenticado')
        self.assertEqual(person_id, id_novo)

    def test_list_persons(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem persons no sistema.
        res = list_persons(conn)
        self.assertFalse(res)

        # Adiciona alguns persons.
        persons = [{'username': 'juanjg', 'first_name': 'juan', 'last_name': 'jorge garcia', 'email': 'juanjg@al.insper.edu.br', 'city': 'rp'},
                   {'username': 'arthurqmo', 'first_name': 'arthur', 'last_name': 'folga', 'email': 'arthurqmo@al.insper.edu.br', 'city': 'sp'}]
        persons_id = []

        for p in persons:
            add_person(conn, p["username"], p["first_name"],
                       p["last_name"], p["email"], p["city"])
            persons_id.append(find_person(conn, p["username"]))

        # Verifica se os persons foram adicionados corretamente.
        res = list_persons(conn)
        self.assertCountEqual(res, persons_id)

        # Remove os persons.
        for p in persons_id:
            remove_person(conn, p)

        # Verifica que todos os persons foram removidos.
        res = list_persons(conn)
        self.assertFalse(res)

    def test_add_bird(self):
        conn = self.__class__.connection

        bird = 'coxinha'

        # Adiciona bird não existente.
        add_bird(conn, bird)

        # Tenta addr a mesma bird duas vezes.
        try:
            add_bird(conn, bird)
            self.fail('Nao deveria ter adicionado a mesma bird duas vezes.')
        except ValueError as e:
            pass

        # Checa se a bird existe.
        id = find_bird(conn, bird)
        self.assertIsNotNone(id)

        # Tenta achar uma bird inexistente.
        id = find_bird(conn, 'esfiha')
        self.assertIsNone(id)

    def test_remove_bird(self):
        conn = self.__class__.connection
        add_bird(conn, 'coxinha')
        id = find_bird(conn, 'coxinha')

        res = list_birds(conn)
        self.assertCountEqual(res, (id,))

        remove_bird(conn, id)

        res = list_birds(conn)
        self.assertFalse(res)

    def test_list_birds(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem birds no sistema.
        res = list_birds(conn)
        self.assertFalse(res)

        # Adiciona algumas birds.
        birds_id = []
        for p in ('abacaxi', 'tomate', 'cebola'):
            add_bird(conn, p)
            birds_id.append(find_bird(conn, p))

        # Verifica se as birds foram adicionadas corretamente.
        res = list_birds(conn)
        self.assertCountEqual(res, birds_id)

        # Remove as birds.
        for c in birds_id:
            remove_bird(conn, c)

        # Verifica que todos as birds foram removidas.
        res = list_birds(conn)
        self.assertFalse(res)

    # @unittest.skip('Em desenvolvimento.')
    def test_add_person_a_bird(self):
        conn = self.__class__.connection

        # Cria algumas birds.
        # add_bird(conn, 'coxinha')
        # id_coxinha = find_bird(conn, 'coxinha')

        # add_bird(conn, 'kibe')
        # id_kibe = find_bird(conn, 'kibe')
        birds = [{'bird_name': 'canario'}, {'bird_name': 'cacatua'}]
        birds_names = []
        for b in birds:
            add_bird(conn, b["bird_name"])
            birds_names.append(find_bird(conn, b["bird_name"]))

        # Cria alguns persons.
        persons = [{'username': 'juanito', 'first_name': 'juan', 'last_name': 'jorge garcia', 'email': 'juanjg@al.insper.edu.br', 'city': 'rp'},
                   {'username': 'arthurolga', 'first_name': 'arthur', 'last_name': 'folga', 'email': 'arthurqmo@al.insper.edu.br', 'city': 'sp'}]
        persons_id = []

        for p in persons:
            add_person(conn, p["username"], p["first_name"],
                       p["last_name"], p["email"], p["city"])
            p_id = find_person(conn, p["username"])
            persons_id.append(p_id)
            # Conecta birds e persons.
            for i in range(len(birds_names)):
                add_bird_to_person(conn, p_id, birds_names[i])
            res = lists_birds_of_person(conn, p_id)
            self.assertCountEqual(res, birds_names)

        # Testa se a remoção de um person causa a remoção das relações entre esse person e suas birds.
        # remove_person(conn, id_viral)

        res = lists_persons_of_bird(conn, birds_names[0])
        self.assertCountEqual(res, persons_id)

        res = lists_persons_of_bird(conn, birds_names[i])
        self.assertCountEqual(res, persons_id)

        # # Testa a remoção específica de uma relação bird-person.
        # remove_person_de_bird(conn, id_estomacal, id_coxinha)

        # res = list_persons_de_bird(conn, id_coxinha)
        # self.assertCountEqual(res, (id_moral,))


def run_sql_script(filename):
    global config
    with open(filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'],
                '-u', config['USER'],
                '-p' + config['PASS'],
                '-h', config['HOST']
            ],
            stdin=f
        )


def setUpModule():
    filenames = [entry for entry in os.listdir()
                 if os.path.isfile(entry) and re.match(r'.*_\d{3}\.sql', entry)]
    for filename in filenames:
        run_sql_script(filename)


def tearDownModule():
    run_sql_script('make_birdbook.sql')


if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)