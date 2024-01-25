from django.db.models import Count, Sum, Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response

from .filters import TransactionFilter
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer


class AccountCursorPagination(CursorPagination):
    page_size = 10
    ordering = "id"


class TransactionCursorPagination(CursorPagination):
    page_size = 10
    ordering = "-timestamp"


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = AccountCursorPagination

    def get_queryset(self):
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        if self.request.user.is_staff:
            return Account.objects.all().annotate(
                transaction_count_last_thirty_days=Count("transaction",
                                                         filter=Q(transaction__timestamp__gte=thirty_days_ago)),
                balance_change_last_thirty_days=Sum("transaction__amount",
                                                    filter=Q(transaction__timestamp__gte=thirty_days_ago))
            )
        else:
            return Account.objects.filter(user=self.request.user).annotate(
                transaction_count_last_thirty_days=Count("transaction",
                                                         filter=Q(transaction__timestamp__gte=thirty_days_ago)),
                balance_change_last_thirty_days=Sum("transaction__amount",
                                                    filter=Q(transaction__timestamp__gte=thirty_days_ago))
            )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TransactionCursorPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        if self.request.user.is_staff:
            return Transaction.objects.all().order_by('-timestamp')
        else:
            return Transaction.objects.filter(account__user=self.request.user).order_by('-timestamp')
