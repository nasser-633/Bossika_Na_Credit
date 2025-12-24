from django.contrib import admin
from .models import LoanRepayment, BusinessLoans
# Register your models here.
admin.site.register(BusinessLoans)
admin.site.register(LoanRepayment)
