from rest_framework import serializers

from .models import Account, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    transaction_count_last_thirty_days = serializers.IntegerField()
    balance_change_last_thirty_days = serializers.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        model = Account
        fields = ['id', 'user', 'name', 'transaction_count_last_thirty_days', 'balance_change_last_thirty_days']
