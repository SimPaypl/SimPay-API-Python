from __future__ import annotations
from typing import TypeVar, Generic
from enum import Enum
from pydantic import BaseModel

T = TypeVar('T')


class RequestMethod(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    HEAD = 'head'
    DELETE = 'delete'
    OPTIONS = 'options'


class ResponsePaginationLinks(BaseModel):
    """Pagination links

    :param next_page: str | None
        Next page link
    :param prev_page: str | None
        Previous page link
    """
    next_page: str | None
    prev_page: str | None


class ResponsePagination(BaseModel):
    """Request pagination

    :param total: int
        Total items in all pages
    :param count: int
        Count of items at current page
    :param per_page: int
        Limit of served items at one page
    :param current_page: int
        Current page
    :param total_pages: int
        Total pages at pagination
    :param links: ResponsePaginationLinks
        Pagination links (next page, previous page)
    """
    total: int
    count: int
    per_page: int
    current_page: int
    total_pages: int
    links: ResponsePaginationLinks


class Response(Generic[T]):
    """Request response

    :param success: bool
        Determinate if request has been procesed successfully
    :param data: any
        Response body data, data can be list of items or object of item
    :param pagination: ResponsePagination | none
        Pagination
    """
    success: bool = False
    data: T | None = None
    pagination: ResponsePagination | None
    
    def has_pagination(self) -> bool:
        return self.pagination is not None
