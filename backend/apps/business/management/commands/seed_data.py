from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from apps.business.models import BusinessProfile
from apps.cashflow.models import CashFlow
from apps.loans.models import BusinessLoans


class Command(BaseCommand):
    help = "Insert dummy data for users, businesses, cashflow and loans"

    def handle(self, *args, **options):
        # NOTE: These passwords are only for development/testing.
        # Do not use them in production.
        users_data = [
            {
                "email": "bossika@gmail.com",
                "password": "1234",
                "username": "bossika",
            },
            {
                "email": "james@gmail.com",
                "password": "456",
                "username": "james",
            },
        ]

        cashflow_data = [
            {
                "cashflow_type": "INCOME",
                "category": "SALES",
                "amount": 6000.00,
                "month": "JAN",
                "date_recorded": "2025-01-12",
            },
            {
                "cashflow_type": "EXPENSE",
                "category": "EMPLOYEE_SALARY",
                "amount": 2000.00,
                "month": "JAN",
                "date_recorded": "2025-01-12",
            },
            {
                "cashflow_type": "LOAN_INFLOW",
                "amount": 1000.00,
                "month": "JAN",
                "date_recorded": "2025-01-12",
            },
        ]

        loans_data = [
            {
                "principal_amount": 1000.00,
                "interest_rate": 0.1,
                "loan_period": 1,
                "lender": "Equity Bank",
            },
        ]

        for u in users_data:
            user, _ = User.objects.get_or_create(
                email=u["email"],
                defaults={"username": u["username"]},
            )

            # Set password correctly (hashing)
            user.set_password(u["password"])
            user.save()

            # Create multiple businesses per user
            business1 = BusinessProfile.objects.create(
                user=user,
                business_name=f"{u['username']}'s First Business",
                size="0-10",
                business_type="SERVICE",
                operation_period=1,
            )

            business2 = BusinessProfile.objects.create(
                user=user,
                business_name=f"{u['username']}'s Second Business",
                size="0-10",
                business_type="RETAIL",
                operation_period=2,
            )

            # Seed cashflow for business1
            for cf in cashflow_data:
                CashFlow.objects.create(
                    business=business1,
                    cashflow_type=cf["cashflow_type"],
                    category=cf.get("category"),
                    amount=cf["amount"],
                    month=cf["month"],
                    date_recorded=cf["date_recorded"],
                )

            # Seed loans for business2
            for loan in loans_data:
                BusinessLoans.objects.create(
                    business=business2,
                    principal_amount=loan["principal_amount"],
                    interest_rate=loan["interest_rate"],
                    loan_period=loan["loan_period"],
                    lender=loan["lender"],
                    category="WORKING_CAPITAL",
                )

        message = "Dummy data inserted successfully!"
        self.stdout.write(self.style.SUCCESS(message))
