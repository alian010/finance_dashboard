from rest_framework.pagination import PageNumberPagination


class TransactionPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"  # optional (max set below)
    max_page_size = 50
