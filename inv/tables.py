import django_tables2 as tables

from .models import Transaction


class TransactionTable(tables.Table):
    parts = tables.Column()

    class Meta:
        model = Transaction
        fields = ('id', 'time', 'parts', 'users', 'approved')
