from functools import wraps

from rest_framework.exceptions import PermissionDenied


def only_admin_check():
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = eval(request.session.get('UserInfo'))
            set1, set2 = set(user['groups']), {'portal_admin'}
            if len(set1.intersection(set2)) == 0:
                raise PermissionDenied('Недостаточно прав')
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
