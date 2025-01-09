from rest_framework.pagination import PageNumberPagination


class FiveItemsPaginator(PageNumberPagination):
    """Типовой пагинатор для постраничного вывода по 5 элементов"""

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100
