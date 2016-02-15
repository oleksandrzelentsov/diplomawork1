from django.db import models
from django.contrib.auth.models import User, AnonymousUser
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
    accesibility = models.ManyToManyField(User, related_name="granted_users", blank=True, null=True)

    def __str__(self):
        return self.name + (" [%s]" % self.category)

    def grant_access(self, *users):
        for user in users:
            if user not in self.accesibility.all() and user is not self.user:
                self.accesibility.add(user)
                self.popularity += 1
                self.save()

    def forbid_access(self, *users):
        for user in users:
            if user in self.accesibility.all():
                self.accesibility.remove(user)
                self.popularity -= 1
                self.save()
            elif user is self.user:
                self.delete()

    @staticmethod
    def average_popularity(selector=lambda x: True):
        coll = [x.popularity for x in Term.objects.all() if selector(x)]
        return sum(coll)/len(coll)

    @staticmethod
    def private_popularity():
        return Term.average_popularity(lambda x: not x.public)

    @staticmethod
    def get_terms(user):
        result = [x for x in Term.objects.all() if x.public]
        if isinstance(user, AnonymousUser) or user is None:
            return result
        private = [x for x in Term.objects.all() if not x.public]
        result += [x for x in private if user in x.accesibility.all()]
        return result


class APIToken(models.Model):
    token = models.TextField(primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return str(self.user)
