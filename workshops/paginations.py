from rest_framework.pagination import PageNumberPagination

class workshop_page(PageNumberPagination):
    page_size = 12
    max_page_size = 10