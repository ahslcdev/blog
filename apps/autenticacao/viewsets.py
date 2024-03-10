from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.response import Response

from apps.autenticacao.serializers import UserSerializerGET, UserSerializerPOST

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializerGET

    def get_queryset(self):
        """ Impedindo que os outros usuários tenham acesso aos dados de outros usuários """
        return super().get_queryset().filter(id=self.request.user.id)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializerPOST
        return super().get_serializer_class()
    
    def get_permissions(self):
        """ Permite que somente o endpoint POST não possuia autenticação ."""
        if self.action == 'create':
            return []
        return super().get_permissions()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Viewset custom pois não é necessário retornar a senha do usuário para o front """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.filter(id=serializer.data.get('id'))
        return Response(UserSerializerGET(user, many=True).data, 201)
    