from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static


class User(AbstractUser):
    fullname = models.CharField(max_length=40, null=True)
    username = models.CharField(max_length=40, unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="static/media/images/avatar.svg", upload_to='images/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def avatar_url(self):
        if self.avatar and str(self.avatar) != "static/media/images/avatar.svg":
            return self.avatar.url
        else:
            return static('media/images/avatar.svg')

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    upvotes = models.ManyToManyField(User, related_name='post_upvotes', blank=True)
    downvotes = models.ManyToManyField(User, related_name='post_downvotes', blank=True)

    @property
    def vote_count(self):
        return self.upvotes.count() - self.downvotes.count()

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.title
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
