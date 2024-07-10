from django_filters import rest_framework as filters
from django.db.models import Q
from portal_api.models import News


class NewsFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    date_gt = filters.DateTimeFilter(field_name='published_date', lookup_expr='gte')
    date_lt = filters.DateTimeFilter(field_name='published_date', lookup_expr='lte')
    author = filters.CharFilter(method='filter_by_author_full_name')

    class Meta:
        model = News
        fields = ['title', 'date_gt', 'date_lt', 'published_date', 'author']

    # Фильтрация по автору
    def filter_by_author_full_name(self, queryset, name, value):
        return queryset.filter(
            Q(user__profile__name__icontains=value) |
            Q(user__profile__surname__icontains=value) |
            Q(user__profile__patronymic__icontains=value)
        )