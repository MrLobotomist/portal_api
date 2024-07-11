import kerberos
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class KerberosAuthView(APIView):
    # Отключение аутентификации и разрешение доступа всем
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Negotiate '):
            return Response({'error': 'Invalid Authorization header'}, status=400)

        auth_token = auth_header[len('Negotiate '):]

        try:
            result, context = kerberos.authGSSServerInit('HTTP')
            if result != kerberos.AUTH_GSS_COMPLETE:
                return Response({'error': 'Kerberos initialization failed'}, status=500)

            result = kerberos.authGSSServerStep(context, auth_token)
            if result != kerberos.AUTH_GSS_COMPLETE:
                return Response({'error': 'Kerberos authentication failed'}, status=401)

            user_principal = kerberos.authGSSServerUserName(context)

            # Assuming the user principal is in the form of username@REALM
            username = user_principal.split('@')[0]

            # Get or create the user
            user, created = User.objects.get_or_create(username=username)

            # Create JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        except kerberos.GSSError as e:
            return Response({'error': str(e)}, status=500)
