from django.db import models

class BaseModel(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')
    ativo = models.BooleanField(default=True, verbose_name='Ativo?')

    class Meta:
        abstract = True