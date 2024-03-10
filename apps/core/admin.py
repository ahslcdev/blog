from django.contrib import admin

from apps.core.models import Comment, Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'autor', 'titulo', 'data_publicacao', 'criado_em', 'atualizado_em')
    list_filter = ('autor', 'data_publicacao',)
    search_fields = ('id', 'autor__username', 'titulo', 'conteudo')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'autor', 'criado_em', 'atualizado_em')
    list_filter = ('autor', 'criado_em',)
    search_fields = ('id', 'autor__username', 'conteudo', )