from django.db import models
from apps.business.models import BusinessProfile
from apps.users.models import TimeStampedModel
from django.db import transaction


class CashFlow(TimeStampedModel):
    MONTH_CHOICES = (
        ('JAN', 'January'),
        ('FEB', 'February'),
        ('MAR', 'March'),
        ('APR', 'April'),
        ('MAY', 'May'),
        ('JUN', 'June'),
        ('JUL', 'July'),
        ('AUG', 'August'),
        ('SEP', 'September'),
        ('OCT', 'October'),
        ('NOV', 'November'),
        ('DEC', 'December'),
    )

    CASHFLOW_TYPES = (
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
        ('LOAN_INFLOW', 'Loan Inflow'),
        ('LOAN_REPAYMENT', 'Loan Repayment'),
    )

    CATEGORY_CHOICES = (
        ('SALES', 'Sales'),
        ('STOCK', 'Stock'),
        ('EMPLOYEE_SALARY', 'Employee Salary'),
    )

    business = models.ForeignKey(
        BusinessProfile,
        on_delete=models.CASCADE,
        related_name='cashflows'
    )

    month = models.CharField(
        max_length=10,
        choices=MONTH_CHOICES,
        null=True,
        blank=True
    )

    year = models.IntegerField(null=True, blank=True)

    is_daily_cashflow = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    cashflow_type = models.CharField(
        max_length=20,
        choices=CASHFLOW_TYPES
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        null=True,
        blank=True
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    date_recorded = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.cashflow_type} - {self.amount}"

    # compute the sign of cash flow
    @property
    def signed_amount(self):
        if self.cashflow_type in ['EXPENSE', 'LOAN_REPAYMENT']:
            return -self.amount
        return self.amount

    # compute balance automatically
    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.balance:
                previous = CashFlow.objects.filter(
                    business=self.business,
                    date_recorded__lt=self.date_recorded
                ).order_by("-date_recorded").first()

                prev_balance = previous.balance if previous else 0
                self.balance = prev_balance + self.signed_amount

            super().save(*args, **kwargs)
