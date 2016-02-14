from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, default=1)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Term(models.Model):
    name = models.CharField(max_length=128)
    definition = models.TextField()
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User, related_name="creator", default=1)
    popularity = models.IntegerField(default=1)
    author = models.ForeignKey(Author, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    public = models.BooleanField(default=False)
    accesibility = models.ManyToManyField(User, related_name="granted_users")

    def __str__(self):
        return self.name + ("[%s]" % self.category)


class APIToken(models.Model):
    token = models.TextField(primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return self.user.first_name
