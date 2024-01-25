import django_filters

from .models import Transaction, TransactionCategory


class TransactionFilter(django_filters.FilterSet):
    start_timestamp = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    end_timestamp = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    account_id = django_filters.NumberFilter(field_name='account__id')
    transaction_category = django_filters.ChoiceFilter(field_name='transaction_category', choices=TransactionCategory.choices)

    class Meta:
        model = Transaction
        fields = ['start_timestamp', 'end_timestamp', 'account_id', 'transaction_category']
