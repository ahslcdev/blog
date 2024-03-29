import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from django.db import transaction
from django.utils.timezone import make_aware
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from apps.core.filters import PostFilter

from apps.core.models import Comment, Post
from apps.core.serializers import CommentsSerializer, CommentsSerializerGET, PostSerializer, PostSerializerGET, PostSerializerPOST

from django_filters.rest_framework import DjangoFilterBackend

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter
    
    def get_queryset(self):
        """
        Override do get_queryset com o objetivo de filtrar as postagens
        com data de publicação maior que data atual.
        """
        queryset = super().get_queryset().filter(
            data_publicacao__lte=make_aware(datetime.datetime.now())
        ).prefetch_related('id_comentarios').only('id', 'titulo', 'autor', 'data_publicacao')
        if self.action not in ['list', 'retrieve']:
            return queryset.filter(autor=self.request.user)
        return queryset

    def get_serializer_class(self):
        """ Dependendo do entpoint, é retornado uma class Serializer """
        if self.action == 'retrieve':
            return PostSerializerGET
        elif self.action in ['update', 'create']:
            return PostSerializerPOST
        return super().get_serializer_class()
    
    @method_decorator(cache_page(30))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        """ Esta viewset foi reescrita devido a utilização dos filtros """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, 200)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ 
        Para está viewset não é necessário enviar o campo AUTOR,
        pois este campo já é capturado pelo usuário logado
        """
        request.data['autor'] = request.user.id
        return super().create(request, *args, **kwargs)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, partial=True, *args, **kwargs)

    @method_decorator(cache_page(30))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer

    def get_queryset(self):
        """
        Override do get_queryset para que em algumas viewsets sejam retornadas queries diferentes
        de acordo com o usuário logado.
        """
        queryset = super().get_queryset().select_related('autor').only('id', 'autor', 'conteudo')
        if self.action not in ['list', 'retrieve']:
            return queryset.filter(autor=self.request.user)
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ 
        Para está viewset não é necessário enviar o campo AUTOR,
        pois este campo já é capturado pelo usuário logado
        Deve-se enviar um atributo id_postagem, que é o id da postagem
        a qual quer associar este comentário.
        """
        request.data['autor'] = request.user.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        postagem = Post.objects.get(id=request.data.get('id_postagem'))
        postagem.id_comentarios.add(serializer.data.get('id'))
        return Response(CommentsSerializerGET(Comment.objects.filter(id=serializer.data.get('id')), many=True).data, 201)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, partial=True, *args, **kwargs)