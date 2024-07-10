from django_filters import rest_framework as filters

from portal_api.models import News


class NewsFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    date_gt = filters.DateTimeFilter(field_name='published_date', lookup_expr='gte')
    date_lt = filters.DateTimeFilter(field_name='published_date', lookup_expr='lte')

    class Meta:
        model = News
        fields = ['title', 'date_gt', 'date_lt', 'published_date']
