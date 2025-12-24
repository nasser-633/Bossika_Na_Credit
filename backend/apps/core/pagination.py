from rest_framework.pagination import PageNumberPagination


class SafePageNumberPagination(PageNumberPagination):
    """
    A PageNumberPagination that avoids importing `coreapi`
    when building schema fields.

    drf-yasg calls `paginator.get_schema_fields(view)` which in
    DRF may require `coreapi`. On Python versions where `coreapi`
    is incompatible, return an empty list so schema generation
    does not raise an exception.
    """

    def get_schema_fields(self, view):
        return []
