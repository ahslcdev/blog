from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class CustomSerializerAccessToken(TokenObtainPairSerializer):

    def validate(self, attr):
        data = super().validate(attr)
        data['usuario'] = self.user.get_username()
        return data
    

class CustomSerializerRefreshToken(TokenRefreshSerializer):

    def validate(self, attr):
        data = super().validate(attr)
        return data
    

class UserSerializerGET(ModelSerializer):
    class Meta:
        fields = [
            'id',
            'username',
            'email'
        ]
        model = User


class UserSerializerPOST(ModelSerializer):
    class Meta:
        fields = [
            'id',
            'username',
            'password',
            'email'
        ]
        model = User

    def validate_password(self, attrs):
        attrs = make_password(attrs)
        return attrs