from functools import wraps

from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response

from portal_api.api_views.common_decorators.only_admin import only_admin_check
from portal_api.filters import UsersFilter
from portal_api.models import CustomPagination
from portal_api.serializers import UserSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter


def change_user_check():
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = eval(request.session.get('UserInfo'))
            set1, set2 = set(user['groups']), {'portal_admin'}
            if len(set1.intersection(set2)) == 0 and request.user.id != int(kwargs['pk']):
                raise PermissionDenied('Недостаточно прав')
            # elif len(set1.intersection(set2)) == 0 and 'groups' in request.data:
            #     raise PermissionDenied('Недостаточно прав на изменение прав)')
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def only_admin_and_user():
    '''
    Проверка только на эндпоинты, содержащие id юзера
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = eval(request.session.get('UserInfo'))
            set1, set2 = set(user['groups']), {'portal_admin'}
            if len(set1.intersection(set2)) == 0 and request.user.id != int(kwargs['pk']):
                raise PermissionDenied('Недостаточно прав')
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


class UserViewSet(viewsets.ModelViewSet):
    queryset = (User.objects.select_related('profile')
                .prefetch_related('groups').all().order_by('date_joined'))
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = UsersFilter
    ordering_fields = ['id', 'email', 'groups', 'profile__surname', 'profile__name', 'profile__patronymic', 'profile__date_of_birth']
    @method_decorator(only_admin_check())
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # TODO не работает ограничение почему-то
    @method_decorator(only_admin_and_user())
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(change_user_check())
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(change_user_check())
    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)
