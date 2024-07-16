import getpass

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class LocalAuth(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        account_name = getpass.getuser().split('@')[0]
        user, created = User.objects.get_or_create(username=account_name)

        # Create JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'id': user.id,
        })
