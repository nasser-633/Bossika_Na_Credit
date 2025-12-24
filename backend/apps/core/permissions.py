from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """Allow access if user is staff or owns the related business object.

    Expects viewsets to filter/query by objects that have a `business` FK
    which itself has a `user` owner.
    """

    def has_permission(self, request, view):
        # allow authenticated users; object-level checks done in has_object_permission
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # admin users may view/manage everything
        if request.user.is_staff or request.user.is_superuser:
            return True

        # object may be a CashFlow, BusinessLoans, or LoanRepayment
        # LoanRepayment -> obj.business_loan.business.user
        business = getattr(obj, 'business', None)
        if business is None:
            # maybe a LoanRepayment
            business_loan = getattr(obj, 'business_loan', None)
            if business_loan is not None:
                business = getattr(business_loan, 'business', None)

        if business is None:
            return False

        return getattr(business, 'user', None) == request.user
