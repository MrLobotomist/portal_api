from django.db.models import Q
from django_filters import rest_framework as filters

from portal_api.models import News, ViewNews
from django.contrib.auth.models import User


class NewsFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    date_gt = filters.DateTimeFilter(field_name='published_date', lookup_expr='gte')
    date_lt = filters.DateTimeFilter(field_name='published_date', lookup_expr='lte')

    class Meta:
        model = News
        fields = ['title', 'date_gt', 'date_lt', 'published_date']


# filterset_fields = ['title', 'user_id', 'published_date', 'author']
class NewsListFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    date_gt = filters.DateFilter(field_name='published_date', lookup_expr='gte')
    date_lt = filters.DateFilter(field_name='published_date', lookup_expr='lte')
    published_date = filters.DateFilter(field_name='published_date', lookup_expr='lte')
    author = filters.CharFilter(lookup_expr='icontains')
    user_id = filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = ViewNews
        fields = ['title', 'date_gt', 'date_lt', 'published_date', 'author']


class UsersFilter(filters.FilterSet):
    id = filters.NumberFilter(lookup_expr='exact')
    email = filters.CharFilter(lookup_expr='icontains')
    groups = filters.CharFilter(field_name='groups__name', lookup_expr='icontains')
    company = filters.CharFilter(field_name='profile__company', lookup_expr='icontains')
    surname = filters.CharFilter(field_name='profile__surname', lookup_expr='icontains')
    name = filters.CharFilter(field_name='profile__name', lookup_expr='icontains')
    patronymic = filters.CharFilter(field_name='profile__patronymic', lookup_expr='icontains')
    date_of_birth = filters.DateFilter(field_name='profile__date_of_birth', lookup_expr='icontains')


    class Meta:
        model = User
        fields = ['id', 'email']
