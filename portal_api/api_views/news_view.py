from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from portal_api.filters import NewsListFilter
from portal_api.models import ViewNews, CustomPagination
from portal_api.serializers import NewsListSerializer


class NewsListView(viewsets.ReadOnlyModelViewSet):
    queryset = ViewNews.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = NewsListSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = NewsListFilter
    ordering_fields = ['published_date', 'title']
