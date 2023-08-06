#!/usr/bin/env python
"""
pagination.py
"""

import logging
from rest_framework.pagination import PageNumberPagination

from drfcommon.response import make_response

logger = logging.getLogger("debug")


class ComStandardPagination(PageNumberPagination):
    """
    Com Standard Pagination
    """
    page_size = 5
    page_size_query_param = 'pagesize'
    max_page_size = 50

    def get_paginated_response(self, data):
        return make_response(
            count=self.page.paginator.count,
            page=self.page.number,
            pages=self.page.paginator.num_pages,
            data={},
            items=data,
        )
