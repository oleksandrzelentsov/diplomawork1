from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=128)

class TermHistory(models.Model):
    author = models.ForeignKey(Author)
    year = models.IntegerField(blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=32)

class Term(models.Model):
    name = models.CharField(max_length=128)
    definition = models.TextField()
    category = models.ForeignKey(Category)
    history = models.ForeignKey(TermHistory, )
