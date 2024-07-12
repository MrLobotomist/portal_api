from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from rest_framework import viewsets
from .serializers import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-name')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
