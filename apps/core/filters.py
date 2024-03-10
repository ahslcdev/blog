# import django_filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend, filters
from django_filters import FilterSet, DateFilter, CharFilter

from apps.core.models import Post

class PostFilter(FilterSet):
    
    data_inicial = DateFilter(field_name="data_publicacao__date", lookup_expr='gte')
    data_final = DateFilter(field_name="data_publicacao__date", lookup_expr='lte')
    search = CharFilter(method='search_filter')

    def search_filter(self, queryset, name, value):
        if value:
            return queryset.filter(Q(autor__username__contains=value) | Q(conteudo__contains=value) | Q(titulo__contains=value))
        return queryset
    
    class Meta:
        model = Post
        fields = (
            'data_inicial', 
            'data_final', 
        )