from rest_framework.pagination import PageNumberPagination

class article_top10_page(PageNumberPagination):
    page_size = 10
    max_page_size = 10

class article_total_page(PageNumberPagination):
    page_size = 20
    max_page_size = 10