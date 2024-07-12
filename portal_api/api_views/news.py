from functools import wraps

from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters import rest_framework as filters

from portal_api.api_views.common_classes.cacheMixin import CacheMixin
from portal_api.filters import NewsFilter
from portal_api.models import News, CustomPagination
from portal_api.serializers import NewsSerializer


def create_check():
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = eval(request.session.get('UserInfo'))
            set1, set2 = set(user['groups']), {'portal_admin', 'portal_writer'}
            if len(set1.intersection(set2)) == 0:
                raise PermissionDenied('Недостаточно прав')
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def upd_and_del_check():
    '''
    Проверка только на эндпоинты, содержащие id юзера
    '''

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = eval(request.session.get('UserInfo'))
            set1, set2 = set(user['groups']), {'portal_admin'}
            try:
                current_news = News.objects.get(id=int(kwargs['pk']))
            except:
                raise NotFound('Статья отсутствует')
            if len(set1.intersection(set2)) == 0 and current_news.user_id != request.user.id:
                raise PermissionDenied('Недостаточно прав')
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


class NewsViewSet(CacheMixin, viewsets.ModelViewSet):
    queryset = (News.objects.select_related('user__profile')
                .only(
        'user_id',
        'title',
        'content',
        'published_date',
        'image',
        'id',
        'user__profile__name',
        'user__profile__surname',
        'user__profile__patronymic'
    ).all().order_by('-published_date'))
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = NewsSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = NewsFilter
    ordering_fields = ['title', 'published_date']

    @method_decorator(create_check())
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(upd_and_del_check())
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(upd_and_del_check())
    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)
