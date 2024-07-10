from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from django.contrib.auth.models import Group, User
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .filters import NewsFilter
from .models import News, CustomPagination, UserProfile
from .permissions import IsCanHandleNews
from .serializers import NewsSerializer, UserSerializer, GroupSerializer, UserProfileSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    permission_classes = [IsAuthenticated, IsCanHandleNews]
    pagination_class = CustomPagination
    serializer_class = NewsSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = NewsFilter
    ordering_fields = ['title', 'published_date']

    def create(self, request, *args, **kwargs):
        if (request.user.groups.filter(name='portal_admin').exists() or
                request.user.groups.filter(name='portal_writer').exists()):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise PermissionDenied('Недостаточно прав')

    def update(self, request, *args, **kwargs):
        if (self.get_object().user == request.user or
                request.user.groups.filter(name='portal_admin').exists()):
            return super().update(request, *args, **kwargs)
        raise PermissionDenied('Недостаточно прав')

    def destroy(self, request, *args, **kwargs):
        if (self.get_object().user == request.user or
                request.user.groups.filter(name='portal_admin').exists()):
            self.perform_destroy(self.get_object())
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied('Недостаточно прав')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name='portal_admin').exists() is False:
            raise PermissionDenied('Недостаточно прав')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if (self.get_object() == request.user or
                request.user.groups.filter(name='portal_admin').exists()):
            return super().update(request, *args, **kwargs)
        raise PermissionDenied('Недостаточно прав')

    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='portal_admin').exists():
            self.perform_destroy(self.get_object())
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied('Недостаточно прав')


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('user_id')
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        data = request.data
        if (request.user.groups.filter(name='portal_admin').exists() is False and
                request.user.id != data['user']):
            raise PermissionDenied('Недостаточно прав')
        data['id'] = data['user']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if (self.get_object().user == request.user or
                request.user.groups.filter(name='portal_admin').exists()):
            return super().update(request, *args, **kwargs)
        raise PermissionDenied('Недостаточно прав')

    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='portal_admin').exists():
            self.perform_destroy(self.get_object())
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied('Недостаточно прав')


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-name')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
