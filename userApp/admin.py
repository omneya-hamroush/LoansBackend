from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from userApp import models


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",

                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "is_loan_customer",
                    "is_loan_provider",
                    "is_bank_personnel",
                ),
            },
        ),

        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "is_loan_customer", "is_loan_provider", "is_bank_personnel"),
            },
        ),
    )
    list_display = [
        "id",
        "email",
        "first_name",
        "last_name",
    ]

    ordering = ("-id",)




admin.site.register(models.User, UserAdmin)
# admin.site.register(models.CustomerUser)
# admin.site.register(models.ProviderUser)
# @admin.register(models.User)
# class UserAdmin(BaseUserAdmin):
#     list_display = [
#         "id",
#         "email",
#         "first_name",
#         "last_name",
#         "is_loan_provider",
#         "is_loan_customer",
#         "is_bank_personnel"
#     ]
#     ordering = ("-id",)
