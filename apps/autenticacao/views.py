from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Permission, Group
from django.contrib import messages
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from apps.exceptions import InvalidUserException

@api_view(['get', 'post'])
@permission_classes([])
def login_page(request):
    if str(request.method == 'POST'):
        usuario = request.POST.get('username')
        senha = request.POST.get('password')
        if senha != None and usuario != None:
            user = authenticate(request, username=usuario, password=senha)
            if user is None:
                return HttpResponse('Usuario não cadastrado, favor checar suas credenciais!', status=404)
            else:
                login(request, user)
                return Response(200)
    return render(request, 'login/login.html')


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')


from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from rest_framework_simplejwt.views import TokenObtainPairView

from apps.autenticacao.serializers import CustomSerializerAccessToken, CustomSerializerRefreshToken

class CustomAccessToken(TokenObtainPairView):
    serializer_class = CustomSerializerAccessToken


class CustomRefreshToken(TokenObtainPairView):
    serializer_class = CustomSerializerRefreshToken