from django.db import models
from django.contrib.auth.models import User
from apps.users.models import TimeStampedModel


class BusinessProfile(TimeStampedModel):

    BUSINESS_TYPE_CHOICES = (
        ('SERVICE', 'Service'),
        ('WHOLESALE', 'Wholesale'),
        ('RETAIL', 'Retail'),
        ('MANUFACTURING', 'Manufacturing'),
        ('TECHNOLOGY', 'Technology'),
    )

    SIZE_CHOICES = (
        ('0-10', '0-10'),
        ('10-20', '10-20'),
        ('20-30', '20-30'),
        ('30-40', '30-40'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='business_profile'
    )

    business_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    business_type = models.CharField(
        max_length=50,
        choices=BUSINESS_TYPE_CHOICES,
        default='SERVICE'
    )

    address = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    size = models.CharField(
        max_length=10,
        choices=SIZE_CHOICES,
        default='0-10'
    )

    # In years (e.g., 0.5 for 6 months)
    operation_period = models.DecimalField(
        max_digits=4,
        decimal_places=1
    )

    def __str__(self):
        return self.business_name or "Unnamed Business"

    @property
    def total_net_cash_flow(self):
        result = self.cashflows.aggregate(
            total=models.Sum(
                models.Case(
                    models.When(
                        cashflow_type__in=['EXPENSE', 'LOAN_REPAYMENT'],
                        then=-models.F('amount')
                    ),
                    default=models.F('amount'),
                    output_field=models.DecimalField()
                )
            )
        )
        return result['total'] or 0
