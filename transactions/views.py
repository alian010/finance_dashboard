from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Transaction
from .serializers import TransactionSerializer
from .permissions import IsOwner
from .pagination import TransactionPagination


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = TransactionPagination

    def get_queryset(self):
        # IMPORTANT: owner-only enforced at queryset level
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # user is set in serializer.create; either way is fine
        serializer.save()
