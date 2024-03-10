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