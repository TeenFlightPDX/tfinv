from django.db import models

from django.contrib.auth.models import User


class Part(models.Model):
    # id field w/ auto-increment primary key automatically set by django

    name = models.CharField(max_length=75, blank=False)
    part_number = models.CharField(max_length=20, blank=False)
    location = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return '%s|%s|%s' % (self.id, self.name, self.part_number)


class Transaction(models.Model):
    # id field w/ auto-increment primary key automatically set by django

    time = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User)
    parts = models.ManyToManyField(Part)

    def __str__(self):
        return '%s|%s' % (self.id, self.parts)
