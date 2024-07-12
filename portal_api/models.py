from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, User
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100, blank=False, null=False)
    surname = models.CharField(max_length=100, blank=False, null=False)
    patronymic = models.CharField(max_length=100, blank=False, null=False)
    position = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=False, null=False)
    image = models.ImageField(upload_to="profile_image/", null=True, blank=True)

    def __str__(self):
        return self.user.username


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='news')
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="news_images/", null=True, blank=True)

    def __str__(self):
        return self.title


class ViewNews(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_news'
