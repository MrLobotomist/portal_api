from functools import wraps

from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, status
from rest_framework.response import Response

from portal_api.models import UserProfile, CustomPagination
from portal_api.serializers import UserProfileSerializer


def create_check():
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = eval(request.session.get('UserInfo'))
            set1, set2 = set(user['groups']), {'portal_admin'}
            if 'user' in request.data:
                id = request.data['user']
            else:
                id = None
            if len(set1.intersection(set2)) == 0 and request.user.id != id and id is not None:
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
            profile_id = UserProfile.objects.get(user_id=request.user.id)
            if len(set1.intersection(set2)) == 0 and profile_id.id != int(kwargs['pk']):
                raise PermissionDenied('Недостаточно прав')
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('user_id')
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @method_decorator(create_check())
    def create(self, request, *args, **kwargs):
        data = request.data
        if 'user' not in request.data:
            data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(upd_and_del_check())
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(upd_and_del_check())
    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)
