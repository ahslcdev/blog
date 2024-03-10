from rest_framework.serializers import ModelSerializer, RelatedField

from apps.core.models import Comment, Post

class PostSerializer(ModelSerializer):
    """ Utilizado na VIEWSET LIST """
    class Meta:
        fields = [
            'id',
            'titulo',
            'get_autor',
            'get_data_publicacao',
        ]
        model = Post
        

class CommentsSerializerGET(ModelSerializer):
    class Meta:
        fields = [
            'id',
            'conteudo',
            'get_autor',
            'get_criado_em'
        ]
        model = Comment


class PostSerializerGET(ModelSerializer):
    """ UTILIZADO NA VIEWSET RETRIEVE"""
    id_comentarios = CommentsSerializerGET(many=True)
    class Meta:
        fields = [
            'id',
            'titulo',
            'get_data_pub',
            'conteudo',
            'id_comentarios'
        ]
        model = Post


class PostSerializerPOST(ModelSerializer):
    """ Utilizado no POST"""
    class Meta:
        fields = [
            'id',
            'titulo',
            'autor',
            'data_publicacao',
            'conteudo'
            # 'comments'
        ]
        model = Post


class CommentsSerializer(ModelSerializer):
    class Meta:
        fields = [
            'id',
            'conteudo',
            'autor',
            'criado_em'
        ]
        model = Comment