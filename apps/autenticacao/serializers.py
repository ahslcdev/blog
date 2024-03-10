from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.serializers import ModelSerializer, ValidationError
# from pesquisa.settings import SIMPLE_JWT


class CustomSerializerAccessToken(TokenObtainPairSerializer):

    def validate(self, attr):
        data = super().validate(attr)
        # data['tempo_vida'] = SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
        data['usuario'] = self.user.get_username()
        return data
    

class CustomSerializerRefreshToken(TokenRefreshSerializer):

    def validate(self, attr):
        data = super().validate(attr)
        # data['tempo_vida'] = SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
        return data