import getpass
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from main.settings import NO_UPDATE_LAST_LOGIN
from django.contrib.auth.models import update_last_login, User
from django.contrib.auth.signals import user_logged_in
from ast import literal_eval
from django.contrib.auth import get_user_model

UserModel = get_user_model()

"""
    Отключение обновления последнего логина
"""
if NO_UPDATE_LAST_LOGIN:
    user_logged_in.disconnect(
        update_last_login, dispatch_uid='update_last_login')

"""
    Мидлвар для отключения CSRF
"""


class DisableCSRFMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response


class SetUserInfo(MiddlewareMixin):
    groups = []
    account_name = ''
    access_token = ''

    def init_from_values(self, values):
        # инициализация списком значений
        val = literal_eval(values)
        # self.negotiate_details = val.get('negotiate_details', "")
        self.account_name = val.get('account_name')
        self.groups = val.get('groups')
        self.access_token = val.get('access_token')

    def process_request(self, request):
        # ищем в кэше уже существующий объект
        # если уже был объект, тогда инициализируемся из него
        values = request.session.get('UserInfo')
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        try:
            auth_type, token = auth_header.split(' ')
        except:
            auth_type, token = False, ''
        if values is None:
            # Попытка получения из jwt
            if auth_header:
                self.get_credentials_from_jwt(request, auth_header)
            else:
                self.account_name = getpass.getuser().split('@')[0]
                user, created = User.objects.get_or_create(username=self.account_name)
                if created:
                    user.set_password('1')
                    user.save()
                self.groups = [group.name for group in user.groups.all()]
                # # формируем авторизацию
                # __, krb_context = kerberos.authGSSClientInit(KERB_REALM)
                # kerberos.authGSSClientStep(krb_context, "")
                # self.negotiate_details = kerberos.authGSSClientResponse(krb_context)
                # сохраняем в сессию значения
                request.session['UserInfo'] = self.__repr__()
        elif self.access_token != token:
            self.get_credentials_from_jwt(request, auth_header)

    def get_credentials_from_jwt(self, request, auth_header):
        try:
            auth_type, token = auth_header.split(' ')
            if auth_type == 'Bearer':
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(token)
                account = jwt_auth.get_user(validated_token)
                if request.user != account:
                    self.account_name = account.username
                    self.groups = [group.name for group in account.groups.all()]
                    self.access_token = token
                    request.session['UserInfo'] = self.__repr__()
                    request.user = account
        except (InvalidToken, TokenError, ValueError):
            request.user = None
            return

    def __repr__(self):
        # вывод данных объекта, для последующего воспроизведения
        lst = {
            "account_name": self.account_name,
            "groups": self.groups,
            "access_token": self.access_token
            # "negotiate": "Negotiate " + self.negotiate_details,
        }
        representation = str(lst)
        return representation
