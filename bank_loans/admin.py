from django.contrib import admin

from bank_loans import models


admin.site.register(models.LoanApplication)
admin.site.register(models.FundApplication)


# class FundInline(admin.StackedInline):
#     model = models.Fund
#
#     readonly_fields = (
#         "amount"
#     )
@admin.register(models.Fund)
class FundAdmin(admin.ModelAdmin):
   list_display = ('id', 'minimum', 'maximum', 'interest_rate', 'duration' )



@admin.register(models.Loan)
class LoanAdmin(admin.ModelAdmin):
   list_display = ('id', 'minimum', 'maximum', 'interest_rate', 'duration' )
   # exclude = ('amount',)
