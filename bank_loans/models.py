from django.db import models
# from .utils import LoanMixin
# Create your models here.


class Loan(models.Model):
    # amount = models.FloatField(null=True, blank=True)
    minimum = models.FloatField(null=True, blank=True)
    maximum = models.FloatField(null=True, blank=True)
    interest_rate = models.FloatField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)


class Fund(models.Model):
    # amount = models.FloatField(null=True, blank=True)
    minimum = models.FloatField(null=True, blank=True)
    maximum = models.FloatField(null=True, blank=True)
    interest_rate = models.FloatField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    # validators=[
    #         MaxValueValidator(100),
    #         MinValueValidator(1)
    #     ]


class LoanApplication(models.Model):
    amount = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=24,
        default="Pending",
        choices=(
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("refused", "Refused"),
            ("finished", "Finished"),

        ),
    )
    user = models.ForeignKey("userApp.User", null=True, on_delete=models.SET_NULL)
    loan = models.ForeignKey("Loan", null=True, on_delete=models.SET_NULL)


class FundApplication(models.Model):
    amount = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=24,
        default="Pending",
        choices=(
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("refused", "Refused"),
            ("finished", "Finished"),

        ),
    )
    user = models.ForeignKey("userApp.User", null=True, on_delete=models.SET_NULL)
    fund = models.ForeignKey("Fund", null=True, on_delete=models.SET_NULL)
