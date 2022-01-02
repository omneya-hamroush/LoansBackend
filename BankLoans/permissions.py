from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist


class ProviderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:

            return request.user.is_loan_provider == True
        except (ObjectDoesNotExist, AttributeError):
            return False


class CustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:

            return request.user.is_loan_customer == True
        except (ObjectDoesNotExist, AttributeError):
            return False


class PersonnelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:

            return request.user.is_bank_personnel == True
        except (ObjectDoesNotExist, AttributeError):
            return False
