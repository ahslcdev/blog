
from django.db import models
from django.contrib.auth.models import User

from apps.base_models import BaseModel

class Comment(BaseModel):
    autor = models.ForeignKey(User, verbose_name='Autor', on_delete=models.CASCADE)
    conteudo = models.TextField(verbose_name='Conteudo')

    @property
    def get_criado_em(self) -> str:
        return self.criado_em.strftime('%d/%m/%Y %H:%M:%S')
    
    @property
    def get_autor(self) -> str:
        return self.autor.username

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-criado_em']


# class PalavrasChaves(BaseModel):
#     nome = models.CharField(max_length=50, verbose_name='Palavras Chaves')


class Post(BaseModel):
    titulo = models.CharField(max_length=255, verbose_name='Título')
    # descricao = models.CharField(max_length=255, verbose_name='Descrição breve', null=True)
    # imagem_capa = models.FileField(verbose_name='Imagem da capa')
    # likes = models.IntegerField(verbose_name='Quantidade de curtidas', default=0)
    conteudo = models.TextField(verbose_name='Conteudo')
    data_publicacao = models.DateTimeField(verbose_name='Data da publicação')
    autor = models.ForeignKey(User, verbose_name='Autor', on_delete=models.CASCADE)
    # id_palavras_chave = models.ManyToManyField
    id_comentarios = models.ManyToManyField(Comment, verbose_name='Comentários', blank=True)

    @property
    def get_data_publicacao(self) -> str:
        return self.data_publicacao.strftime('%d/%m/%Y %H:%M:%S')
    
    @property
    def get_data_pub(self) -> str:
        return self.data_publicacao.strftime('%Y-%m-%d %H:%M')
    
    @property
    def get_autor(self) -> str:
        return self.autor.username
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-data_publicacao']


