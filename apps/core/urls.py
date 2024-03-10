from django.urls import path

from apps.core.views import add_post, change_comment, index, view_post

urlpatterns = [
    path('', index, name='index'),
    path('post/change/<int:pk>', view_post, name='view_post'),
    path('post/add/', add_post, name='add_post'),
    path('comments/change/<int:pk>', change_comment, name='change_comment')
]