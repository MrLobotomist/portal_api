from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group, User
from rest_framework import viewsets
from .models import News, GroupSerializer, CustomPagination
from .permissions import IsCanDelete
from .serializers import NewsSerializer, UserSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated, IsCanDelete]
    pagination_class = CustomPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
