import django_filters as filters
from django.contrib.auth import models as auth_models
from graphene_django_extras.filters import SearchFilterSet


class UserFilterSet(filters.FilterSet):
    class Meta:
        model = auth_models.User
        fields = {
            "id": ("exact",),
            "first_name": ("icontains", "iexact"),
            "last_name": ("icontains", "iexact"),
            "username": ("icontains", "iexact"),
            "email": ("icontains", "iexact"),
            "is_staff": ("exact",),
        }


class UserSearchFilterSet(SearchFilterSet):
    class Meta:
        model = auth_models.User
        search_fields = ["first_name", "last_name"]
        fields = []
