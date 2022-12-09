from rest_framework.pagination import PageNumberPagination

class article_top10_page(PageNumberPagination):
    # page_size = 9
    page_size = 10
    # test용 개수 4개
    max_page_size = 10

class article_total_page(PageNumberPagination):
    page_size = 20
    max_page_size = 10