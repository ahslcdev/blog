from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from rest_framework_simplejwt.views import TokenObtainPairView

from apps.autenticacao.serializers import CustomSerializerAccessToken, CustomSerializerRefreshToken

@api_view(['get', 'post'])
@permission_classes([])
def login_page(request):
    if str(request.method == 'POST'):
        usuario = request.POST.get('username')
        senha = request.POST.get('password')
        if senha != None and usuario != None:
            user = authenticate(request, username=usuario, password=senha)
            if user is None:
                return Response(status=404)
            else:
                login(request, user)
                return Response(200)
    return render(request, 'login/login.html')


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')

def add_user(request):
    return render(request, 'user/add.html')

class CustomAccessToken(TokenObtainPairView):
    """ 
    Ao utilizar esta uma classe custom para obter o token de acesso, 
    concede ao desenvolvedor a opção de poder customizar os retornos
    podendo adicionar outros campos que possa considerar úteis, em outras palavras,
    permite adicionar novas lógicas.
    """
    serializer_class = CustomSerializerAccessToken


class CustomRefreshToken(TokenObtainPairView):
    serializer_class = CustomSerializerRefreshToken