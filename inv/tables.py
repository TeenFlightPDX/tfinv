import django_tables2 as tables

from .models import Transaction, PartChange


class TransactionTable(tables.Table):
    parts = tables.Column(orderable=False)

    view = tables.TemplateColumn(
        '<a href="{% url "inv:transaction_view" id=record.id %}" class="btn btn-primary">View</a>',
        orderable=False,
        verbose_name='')

    class Meta:
        model = Transaction
        fields = ('id', 'time', 'parts', 'user', 'approved', 'view')


class PartChangeTable(tables.Table):
    class Meta:
        model = PartChange
        fields = ('name', 'part_number', 'location', 'quantity')
