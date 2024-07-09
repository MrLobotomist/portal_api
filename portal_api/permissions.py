from rest_framework.permissions import BasePermission


class IsCanDelete(BasePermission):
    """
    Проверяет на возможность удаления
    """

    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.groups.filter(name='portal_admin').exists()
        if request.method in ['POST', 'PUT', 'PATCH']:
            return (request.user.groups.filter(name='portal_writer').exists() or
                    request.user.groups.filter(name='portal_admin').exists())
        return True
