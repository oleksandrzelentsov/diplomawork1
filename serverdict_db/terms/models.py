from django.contrib.auth.models import User, AnonymousUser
from django.db import models


# Create your models here.
from django.db.models import Q


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
    accessibility = models.ManyToManyField(User, related_name="granted_users", blank=True)
    date_added = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name + (" [%s]" % self.category)

    def make_public(self):
        """Called when the term is so approved that it's time to
        make it public."""
        self.public = True
        self.accessibility.clear()

    def reset(self):
        """Called when the term is edited and is losing all it's
        popularity due to updating fields."""
        self.public = False
        self.accessibility.clear()
        self.accessibility.add(self.user)

    def grant_access(self, *users):
        for user in users:
            if user not in self.accessibility.all() and user is not self.user:
                self.accessibility.add(user)
                self.popularity += 1
                if self.popularity > Term.average_popularity():
                    self.make_public()
                    self.save()
                    return
        self.save()

    def forbid_access(self, *users):
        for user in users:
            if user in self.accessibility.all():
                self.accessibility.remove(user)
                self.popularity -= 1
            elif user is self.user:
                self.delete()
                return
        self.save()

    def is_accessible(self, user: User):
        if self.public or user in self.accessibility.all() or user.is_superuser:
            return True
        else:
            return False

    @staticmethod
    def average_popularity(selector=lambda x: True):
        coll = [x.popularity for x in Term.objects.all() if selector(x)]
        return sum(coll)/len(coll)

    @staticmethod
    def private_popularity():
        return Term.average_popularity(lambda x: not x.public)

    @staticmethod
    def get_terms(user):
        if user.is_superuser:
            return Term.objects.all()
        result = Term.objects.filter(Q(public__exact=True) | Q(accessibility__in=[user.id]))
        return result


class APIToken(models.Model):
    token = models.TextField(primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return str(self.user)
