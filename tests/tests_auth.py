import json
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class TestAuthSession(TestCase):
    """ Esta classe de teste serve para testar as VIEWS de autenticação e autorização que utilizam SESSION"""
    def setUp(self) -> None:
        """ Definindo as bases para os testes """
        self.client = APIClient()
        self.dados_login_success = {
            "username":"teste",
            "password":"teste"
        }
        self.dados_login_error = {
            "username":"teste2",
            "password":"teste"
        }
        self.user = User.objects.create(
            username=self.dados_login_success['username'],
            password=make_password(self.dados_login_success['password'])
        )
        return super().setUp()
    
    def test_login_success(self):
        """ Teste de sucesso no login """
        response = self.client.post(f'/autenticacao/login/', self.dados_login_success)
        self.assertTrue(response.status_code == 200)

    def test_login_error(self):
        """ Teste de error no login, geralmente ocasionado pelo usuário não ser encontrado """
        response = self.client.post(f'/autenticacao/login/', self.dados_login_error)
        self.assertTrue(response.status_code == 404)

    def test_logout(self):
        """ Teste de logout do sistema """
        response = self.client.post(f'/autenticacao/logout/', self.dados_login_success)
        self.assertTrue(response.status_code == 302)


class TestAuthJWT(TestCase):
    """ Esta classe de teste serve para testar as VIEWSETS da API, que utiliza JWT """
    def setUp(self) -> None:
        """ Definindo as bases para os testes """
        self.client = APIClient()
        self.dados_login_success = {
            "username":"teste",
            "password":"teste"
        }
        self.dados_login_error = {
            "username":"teste2",
            "password":"teste"
        }
        self.dados_vazio = {
            "username":"",
            "password":""
        }
        self.user = User.objects.create(
            username=self.dados_login_success['username'],
            password=make_password(self.dados_login_success['password'])
        )
        return super().setUp()
    
    def test_login_success(self):
        """ Teste de sucesso no login """
        response = self.client.post(f'/autenticacao/token/', self.dados_login_success)
        self.assertTrue(response.status_code == 200)

    def test_login_error(self):
        """ Teste de error no login, geralmente ocasionado pelo usuário não ser encontrado """
        response = self.client.post(f'/autenticacao/token/', self.dados_login_error)
        self.assertTrue(response.status_code == 401)

    def test_login_error_empty(self):
        """ Teste de error no login ao enviar um json vazio """
        response = self.client.post(f'/autenticacao/token/', self.dados_vazio)
        self.assertTrue(response.status_code == 400)

    def test_blacklist_error_400(self):
        """ Teste de logout do sistema """
        response = self.client.post(f'/autenticacao/blacklist/', self.dados_login_success)
        self.assertTrue(response.status_code == 400)

    def test_blacklist_error_401(self):
        """ Teste de adicionar JWT na blacklist com um TOKEN REFRESH INVÁLIDO. """
        login = self.client.post(f'/autenticacao/token/', self.dados_login_success)
        refresh = {
            "refresh":login.json().get('refresh')+'12321312'
        }
        response = self.client.post(f'/autenticacao/blacklist/', refresh)
        self.assertTrue(response.status_code == 401)

    def test_blacklist_sucess(self):
        """ Teste de adicionar JWT na blacklist com sucesso """
        login = self.client.post(f'/autenticacao/token/', self.dados_login_success)
        refresh = {
            "refresh":login.json().get('refresh')
        }
        response = self.client.post(f'/autenticacao/blacklist/', refresh)
        self.assertTrue(response.status_code == 200)

    def test_refresh_error_401(self):
        """ Teste de error para obter um novo refresh token """
        login = self.client.post(f'/autenticacao/token/', self.dados_login_success)
        refresh = {
            "refresh":login.json().get('refresh')+'12312'
        }
        response = self.client.post(f'/autenticacao/token/refresh/', refresh)
        self.assertTrue(response.status_code == 401)

    def test_refresh_error_400(self):
        """ Teste de error para obter um novo refresh token """
        login = self.client.post(f'/autenticacao/token/', self.dados_login_success)
        refresh = {
            "refresh":''
        }
        response = self.client.post(f'/autenticacao/token/refresh/', refresh)
        self.assertTrue(response.status_code == 400)

    def test_refresh_success(self):
        """ Teste de error para obter um novo refresh token """
        login = self.client.post(f'/autenticacao/token/', self.dados_login_success)
        refresh = {
            "refresh":login.json().get('refresh')
        }
        response = self.client.post(f'/autenticacao/token/refresh/', refresh)
        self.assertTrue(response.status_code == 200)


class TestUsers(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.dados_cliente = {
            "username":"teste2",
            "password":"teste"
        }
        self.dados_vazio = {
            "username":"",
            "password":""
        }
        self.user = User.objects.create(
            username="teste2",
            password=make_password('teste'),
            email="teste@gmail.com"
        )

        self.novo_user = User.objects.create(
            username="teste23",
            password=make_password('teste'),
            email="teste3@gmail.com"
        )
        self.login = self.client.post(f'/autenticacao/token/', self.dados_cliente).json()
        return super().setUp()

    def test_create_user_success(self):
        response = self.client.post(f'/api-users/users/', self.dados_cliente)
        self.assertTrue(response.status_code, 201)

    def test_create_user_error_400(self):
        """ 
        Teste de criação de usuário com o envio de dados vazio e com a tentativa de criação de usuario
        com o username já existente
        """
        response = self.client.post(f'/api-users/users/', self.dados_vazio)
        self.assertTrue(response.status_code, 400)

        self.client.post(f'/api-users/users/', self.dados_cliente)
        response = self.client.post(f'/api-users/users/', self.dados_cliente)
        self.assertTrue(response.status_code, 400)

    def test_create_user_error_400(self):
        response = self.client.post(f'/api-users/users/', self.dados_vazio)
        self.assertTrue(response.status_code, 400)

    def test_users_list_success(self):
        """ Teste de sucesso na listagem de usuários"""
        response = self.client.get(f'/api-users/users/', {}, headers={"Authorization":f'Bearer {self.login.get("access")}'})
        self.assertTrue(response.status_code == 200) 
        self.assertTrue(isinstance(response.json(), list))

    def test_users_retrieve_success(self):
        """ Teste de sucesso na listagem de usuário específico """
        response = self.client.get(f'/api-users/users/{self.user.id}/', {}, headers={"Authorization":f'Bearer {self.login.get("access")}'})
        self.assertTrue(response.status_code == 200)
        self.assertTrue(isinstance(response.json(), dict))

    def test_users_retrieve_error(self):
        """ Teste de error ao tentar acessar um usuário inexistente """
        response = self.client.get(f'/api-users/users/150000000000/', {}, headers={"Authorization":f'Bearer {self.login.get("access")}'})
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))

    def test_users_update_success(self):
        """ Teste de sucesso para atualizar um usuário """
        email_antes = self.user.email
        self.dados_cliente['email'] = 'teste2@gmail.com'
        response = self.client.put(
            f'/api-users/users/{self.user.id}/', 
            json.dumps(self.dados_cliente),
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        
        self.assertTrue(response.status_code == 200)
        self.assertTrue(isinstance(response.json(), dict))
        self.assertTrue(email_antes != response.json().get('email'))

    def test_users_update_error(self):
        """ Teste de error para atualizar um usuário 
            Neste teste serão verificadas 2 situações:
            - 1: Tentar atualizar um usuário que não existe
            - 2: Tentar atualizar um usuário de outro autor
            Deve retornar 404 em ambas as situações.
        """
        self.dados_cliente['email'] = 'teste@gmail.com'

        # Atualizar usuário que não existe
        response = self.client.put(
            f'/api-users/users/500000/', 
            json.dumps(self.dados_cliente),
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))

        # Atualizar usuário de outro usuário
        response = self.client.put(
            f'/api-users/users/{self.novo_user.id}/', 
            json.dumps(self.dados_cliente),
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))

    def test_users_delete_success(self):
        """ Teste de sucesso para deletar um usuário """
        response = self.client.delete(
            f'/api-users/users/{self.user.id}', 
            # content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 301)

    def test_users_delete_error(self):
        """ Teste de error para deletar um usuário 
            Neste teste serão verificadas 2 situações:
            - 1: Tentar deletar um usuário que não existe
            - 2: Tentar deletar um usuário de outro autor
            Deve retornar 404 em ambas as situações.
        """
        # Deletar postagem que não existe
        response = self.client.delete(
            f'/api-users/users/500000/', 
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))

        # Deletar postagem de outro autor
        response = self.client.delete(
            f'/api-users/users/{self.novo_user.id}/', 
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))

        