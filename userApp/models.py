from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy as _


# class UserMixin(AbstractUser):
#     email = models.EmailField(verbose_name="email address", unique=True,)
#     username = models.CharField(_("username"), max_length=150,)
#     is_active = models.BooleanField(default=True)
#     EMAIL_FIELD = "email"
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]




class CustomUserManager(UserManager):
    def create_user(self, email, first_name, last_name, username, password, **kwargs):
        # if not email:
        #     raise ValueError('User must have an email address')
        #
        # user = self.model(
        #     email=self.normalize_email(email),
        #     first_name=first_name,
        #     last_name=last_name,
        #     username=username,
        #
        #     **kwargs
        # )
        # user.set_password(self.cleaned_data["password"])
        user = self.create_user(
        email,
        first_name,
        last_name,
        password=password,
        )
        user.save()
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields["is_active"] = True
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(verbose_name="email address", unique=True,)
    username = models.CharField(_("username"), max_length=150,)
    is_active = models.BooleanField(default=True)
    is_loan_provider = models.BooleanField(default=False)
    is_loan_customer = models.BooleanField(default=False)
    is_bank_personnel = models.BooleanField(default=False)


    # verification_code = models.CharField(
    #     max_length=10, default=rand_int_4digits, null=True, blank=True
    # )

    # password_reset_code = models.CharField(max_length=10, null=True, blank=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]



class CustomerUser(models.Model):
    # loan = models.ManyToManyField(
    #     "bank_loans.Loan", related_name="customer_loans", blank=True
    # )
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, blank=True, null=True
    )

class ProviderUser(models.Model):
    # fund = models.ManyToManyField(
    #     "bank_loans.Fund", related_name="provider_loans", blank=True
    # )
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, blank=True, null=True
    )
