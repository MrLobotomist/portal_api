from rest_framework import serializers
from django.contrib.auth.models import User, Group

from .models import News, UserProfile, ViewNews


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = News
        fields = '__all__'

    def get_author(self, obj):
        if obj.user is not None:
            data = obj.user.profile
            return f"{data.surname} {data.name} {data.patronymic}"
        return None


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all()
    )
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups', 'profile']


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewNews
        fields = '__all__'
