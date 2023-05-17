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
    next_page: str | None
    prev_page: str | None


class ResponsePagination(BaseModel):
    total: int
    count: int
    per_page: int
    current_page: int
    total_pages: int
    links: ResponsePaginationLinks


class Response(Generic[T]):
    success: bool = False
    data: T | None = None
    pagination: ResponsePagination | None
    
    def has_pagination(self) -> bool:
        return self.pagination is not None
