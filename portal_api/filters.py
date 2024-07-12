from django.db.models import Q
from django_filters import rest_framework as filters

from portal_api.models import News, ViewNews


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
    date_gt = filters.DateTimeFilter(field_name='published_date', lookup_expr='gte')
    date_lt = filters.DateTimeFilter(field_name='published_date', lookup_expr='lte')
    author = filters.CharFilter(lookup_expr='icontains')
    user_id = filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = ViewNews
        fields = ['title', 'date_gt', 'date_lt', 'published_date', 'author']
