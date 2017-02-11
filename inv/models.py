from django.db import models

from django.contrib.auth.models import User


class Transaction(models.Model):
    # id field w/ auto-increment foreign key automatically set by django

    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, unique=False)
    approved = models.BooleanField(default=False)

    def getParts(self):
        return PartChange.objects.filter(transaction=self)

    def __str__(self):
        return '%s|%s' % (self.id, self.getParts())

    @property
    def parts(self):
        parts_all = self.getParts()
        parts_len = parts_all.count()

        if parts_len > 5:
            parts = [p.part_number for p in self.getParts()[:4]]
            parts.append('...')
        else:
            parts = [p.part_number for p in self.getParts()[:5]]

        return ', '.join(parts)

    @property
    def parts_all(self):
        return ', '.join(self.getParts())


# In the future, we might want to make it so that the same part does not get multiple entries in different transactions
class PartChange(models.Model):
    # Currently, each PartChange is tied to a specific transaction
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    name = models.CharField(max_length=75, blank=False)
    part_number = models.CharField(max_length=20, blank=False)
    location = models.CharField(max_length=20, blank=True)
    quantity = models.IntegerField(blank=False, default=1)

    def __str__(self):
        return '%s|%s|%s' % (self.id, self.name, self.part_number)
