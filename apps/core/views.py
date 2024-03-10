from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.core.models import Comment, Post

# Create your views here.
def index(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def view_post(request, pk):
    data = {
        'id':pk,
        'dono': True if Post.objects.filter(autor=request.user, id=pk) else False
    }
    return render(request, 'posts/change.html', data)


@login_required(login_url='login')
def add_post(request):
    return render(request, 'posts/add.html')


@login_required(login_url='login')
def change_comment(request, pk):
    data = {
        'id':pk,
        'dono': True if Comment.objects.filter(autor=request.user, id=pk) else False
    }
    return render(request, 'comments/change.html', data)