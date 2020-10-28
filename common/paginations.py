from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PathPagePagination(PageNumberPagination):
    """
    自定义分页器
    """
    page = 10  # 默认返回10条数据
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 50  # 最多返回50条数据

    def paginate_queryset(self, queryset, request, view=None):
        # 将路由中的分页参数放到query_params
        query_params = request.query_params.copy()
        query_params.update(**request.parser_context['kwargs'])
        request._request.GET = query_params
        return super().paginate_queryset(queryset, request, view)

    # 改写分页结果返回
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'list': data,
            'page': self.page.number,
            'pages': self.page.paginator.num_pages,
        })
