import datetime
import json
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.timezone import make_aware
from apps.core.models import Comment, Post

class TestPosts(TestCase):
    """ Classe de teste para os endpoints de POSTAGEM 
        Para os testes serão considerados o STATUS_CODE do response e em alguns testes
        serão considerados também o tipo de retorno.
    """
    def setUp(self) -> None:

        self.client = APIClient()

        self.dados_login = {
            'username':'teste',
            'password':'teste'
        }

        self.user = User.objects.create(
            username=self.dados_login['username'],
            password=make_password(self.dados_login['password'])
        )
        self.dados_post_success = {
            'autor':self.user,
            'titulo':'Titulo postagem top',
            'conteudo':'Conteudo top',
            'data_publicacao':str(make_aware(datetime.datetime.now()))
        }
        
        self.postagem = Post.objects.create(
           **self.dados_post_success
        )

        novo_autor = User.objects.create(
            username='teste2',
            password=make_password(self.dados_login['password'])
        )
        dados_novo_autor = self.dados_post_success.copy()
        dados_novo_autor['autor'] = novo_autor

        self.postagem_novo_autor = Post.objects.create(
           **dados_novo_autor
        )
        self.login = self.client.post(f'/autenticacao/token/', self.dados_login).json()


    def test_post_CRUD_no_auth(self):
        """ Teste para garantir que não é possível realizar as operações de CRUD sem está logado.
            Note que nos teste de DELETE E PUT, estou passando um ID inválido e mesmo assim não é possível
            prosseguir com a operação pois o usuário não está logado.
        """
        response = self.client.get(f'/api/posts/', {})
        self.assertTrue(response.status_code == 401)

        response = self.client.post(f'/api/posts/', {})
        self.assertTrue(response.status_code == 401)

        response = self.client.delete(f'/api/posts/1/', {})
        self.assertTrue(response.status_code == 401)

        response = self.client.put(f'/api/posts/1/', {})
        self.assertTrue(response.status_code == 401)

    def test_post_list_success(self):
        """ Teste de sucesso na listagem de postagens"""
        response = self.client.get(f'/api/posts/', {}, headers={"Authorization":f'Bearer {self.login.get("access")}'})
        self.assertTrue(response.status_code == 200) 
        self.assertTrue(isinstance(response.json(), list))

    def test_post_retrieve_success(self):
        """ Teste de sucesso na listagem de postagem específica """
        response = self.client.get(f'/api/posts/{self.postagem.id}/', {}, headers={"Authorization":f'Bearer {self.login.get("access")}'})
        self.assertTrue(response.status_code == 200)
        self.assertTrue(isinstance(response.json(), dict))

    def test_post_retrieve_error(self):
        """ Teste de error ao tentar acessar uma postagem inexistente """
        response = self.client.get(f'/api/posts/150000000000/', {}, headers={"Authorization":f'Bearer {self.login.get("access")}'})
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))

    def test_post_create_success(self):
        """ Teste de sucesso para criar uma postagem"""
        self.dados_post_success['autor'] = self.user.id
        response = self.client.post(
            f'/api/posts/', 
            json.dumps(self.dados_post_success),
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 201)
        self.assertTrue(isinstance(response.json(), dict))

    def test_post_create_error_validation_data(self):
        """ Teste de error para tentar criar postagem sem os valores de cada campo """
        self.dados_post_success['autor'] = self.user.id
        response = self.client.post(
            f'/api/posts/', 
            json.dumps({}),
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 400)
        self.assertTrue(isinstance(response.json(), dict))

    def test_post_update_success(self):
        """ Teste de sucesso para atualizar uma postagem """
        conteudo_antes = self.postagem.conteudo
        self.dados_post_success['conteudo'] = 'Novo conteudo'
        self.dados_post_success['autor'] = self.user.id
        response = self.client.put(
            f'/api/posts/{self.postagem.id}/', 
            json.dumps(self.dados_post_success),
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        
        self.assertTrue(response.status_code == 200)
        self.assertTrue(isinstance(response.json(), dict))
        self.assertTrue(conteudo_antes != response.json().get('conteudo'))

    def test_post_update_error(self):
        """ Teste de error para atualizar uma postagem 
            Neste teste serão verificadas 2 situações:
            - 1: Tentar atualizar uma postagem que não existe
            - 2: Tentar atualizar uma postagem de outro autor
            Deve retornar 404 em ambas as situações.
        """
        self.dados_post_success['conteudo'] = 'Novo conteudo'
        self.dados_post_success['autor'] = self.user.id

        # Atualizar postagem que não existe
        response = self.client.put(
            f'/api/posts/500000/', 
            json.dumps(self.dados_post_success),
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))

        # Atualizar postagem de outro autor
        response = self.client.put(
            f'/api/posts/{self.postagem_novo_autor.id}/', 
            json.dumps(self.dados_post_success),
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))

    def test_post_delete_success(self):
        """ Teste de sucesso para deletar uma postagem """
        self.dados_post_success['autor'] = self.user.id
        response = self.client.put(
            f'/api/posts/{self.postagem.id}/', 
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        
        self.assertTrue(response.status_code == 200)
        self.assertTrue(isinstance(response.json(), dict))

    def test_post_delete_error(self):
        """ Teste de error para deletar uma postagem 
            Neste teste serão verificadas 2 situações:
            - 1: Tentar deletar uma postagem que não existe
            - 2: Tentar deletar uma postagem de outro autor
            Deve retornar 404 em ambas as situações.
        """
        self.dados_post_success['autor'] = self.user.id

        # Deletar postagem que não existe
        response = self.client.put(
            f'/api/posts/500000/', 
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))

        # Deletar postagem de outro autor
        response = self.client.put(
            f'/api/posts/{self.postagem_novo_autor.id}/', 
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))


class TestComments(TestCase):
    """ Classe de teste para os endpoints de COMENTARIOS 
        Para os testes serão considerados o STATUS_CODE do response e em alguns testes
        serão considerados também o tipo de retorno.
    """
    def setUp(self) -> None:

        self.client = APIClient()

        self.dados_login = {
            'username':'teste',
            'password':'teste'
        }

        self.user = User.objects.create(
            username=self.dados_login['username'],
            password=make_password(self.dados_login['password'])
        )
        
        self.dados_post_success = {
            'autor':self.user,
            'titulo':'Titulo postagem top',
            'conteudo':'Conteudo top',
            'data_publicacao':str(make_aware(datetime.datetime.now()))
        }
        
        self.postagem = Post.objects.create(
           **self.dados_post_success
        )

        self.dados_comment_success = {
            'autor':self.user,
            'conteudo':'Conteudo top'
        }
        
        self.comentario = Comment.objects.create(
           **self.dados_comment_success
        )

        novo_autor = User.objects.create(
            username='teste2',
            password=make_password(self.dados_login['password'])
        )
        dados_novo_autor = self.dados_comment_success.copy()
        dados_novo_autor['autor'] = novo_autor

        self.comentario_novo_autor = Comment.objects.create(
           **dados_novo_autor
        )
        self.login = self.client.post(f'/autenticacao/token/', self.dados_login).json()


    def test_comments_CRUD_no_auth(self):
        """ Teste para garantir que não é possível realizar as operações de CRUD sem está logado.
            Note que nos teste de DELETE E PUT, estou passando um ID inválido e mesmo assim não é possível
            prosseguir com a operação pois o usuário não está logado.
        """
        response = self.client.get(f'/api/comments/', {})
        self.assertTrue(response.status_code == 401)

        response = self.client.post(f'/api/comments/', {})
        self.assertTrue(response.status_code == 401)

        response = self.client.delete(f'/api/comments/1/', {})
        self.assertTrue(response.status_code == 401)

        response = self.client.put(f'/api/comments/1/', {})
        self.assertTrue(response.status_code == 401)

    def test_comments_list_success(self):
        """ Teste de sucesso na listagem de comentarios"""
        response = self.client.get(f'/api/comments/', {}, headers={"Authorization":f'Bearer {self.login.get("access")}'})
        self.assertTrue(response.status_code == 200) 
        self.assertTrue(isinstance(response.json(), list))

    def test_comments_retrieve_success(self):
        """ Teste de sucesso na listagem de comentario específico """
        response = self.client.get(f'/api/comments/{self.comentario.id}/', {}, headers={"Authorization":f'Bearer {self.login.get("access")}'})
        self.assertTrue(response.status_code == 200)
        self.assertTrue(isinstance(response.json(), dict))

    def test_comments_retrieve_error(self):
        """ Teste de error ao tentar acessar um comentario inexistente """
        response = self.client.get(f'/api/comments/150000000000/', {}, headers={"Authorization":f'Bearer {self.login.get("access")}'})
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))

    def test_comments_create_success(self):
        """ Teste de sucesso para criar um comentario"""
        self.dados_comment_success['autor'] = self.user.id
        self.dados_comment_success['id_postagem'] = self.postagem.id
        response = self.client.post(
            f'/api/comments/', 
            json.dumps(self.dados_comment_success),
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 201)
        self.assertTrue(isinstance(response.json(), list))

    def test_comments_create_error_validation_data(self):
        """ Teste de error para tentar criar comentario sem os valores de cada campo """
        self.dados_comment_success['autor'] = self.user.id
        response = self.client.post(
            f'/api/comments/', 
            json.dumps({}),
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 400)
        self.assertTrue(isinstance(response.json(), dict))

    def test_comments_update_success(self):
        """ Teste de sucesso para atualizar um comentario """
        conteudo_antes = self.comentario.conteudo
        self.dados_comment_success['conteudo'] = 'Novo conteudo'
        self.dados_comment_success['autor'] = self.user.id
        response = self.client.put(
            f'/api/comments/{self.comentario.id}/', 
            json.dumps(self.dados_comment_success),
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        
        self.assertTrue(response.status_code == 200)
        self.assertTrue(isinstance(response.json(), dict))
        self.assertTrue(conteudo_antes != response.json().get('conteudo'))

    def test_comments_update_error(self):
        """ Teste de error para atualizar um comentario 
            Neste teste serão verificadas 2 situações:
            - 1: Tentar atualizar um comentario que não existe
            - 2: Tentar atualizar um comentario de outro autor
            Deve retornar 404 em ambas as situações.
        """
        self.dados_comment_success['conteudo'] = 'Novo conteudo'
        self.dados_comment_success['autor'] = self.user.id

        # Atualizar comentario que não existe
        response = self.client.put(
            f'/api/comments/500000/', 
            json.dumps(self.dados_comment_success),
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))

        # Atualizar comentario de outro autor
        response = self.client.put(
            f'/api/comments/{self.comentario_novo_autor.id}/', 
            json.dumps(self.dados_comment_success),
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))

    def test_comments_delete_success(self):
        """ Teste de sucesso para deletar um comentario """
        self.dados_comment_success['autor'] = self.user.id
        response = self.client.put(
            f'/api/comments/{self.comentario.id}/', 
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        
        self.assertTrue(response.status_code == 200)
        self.assertTrue(isinstance(response.json(), dict))

    def test_comments_delete_error(self):
        """ Teste de error para deletar um comentario 
            Neste teste serão verificadas 2 situações:
            - 1: Tentar deletar um comentario que não existe
            - 2: Tentar deletar um comentario de outro autor
            Deve retornar 404 em ambas as situações.
        """
        self.dados_comment_success['autor'] = self.user.id

        # Deletar comentario que não existe
        response = self.client.put(
            f'/api/comments/500000/', 
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))

        # Deletar comentario de outro autor
        response = self.client.put(
            f'/api/comments/{self.comentario_novo_autor.id}/', 
            content_type='application/json',
            headers={
                "Authorization":f'Bearer {self.login.get("access")}'
            }
        )
        self.assertTrue(response.status_code == 404)
        self.assertTrue(isinstance(response.json(), dict))