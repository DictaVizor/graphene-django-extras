# -*- coding: utf-8 -*-
import operator
from django_filters.filterset import BaseFilterSet, FilterSet, FilterSetMetaclass, FilterSetOptions
from django_filters import CharFilter
from django_filters.filterset import FILTER_FOR_DBFIELD_DEFAULTS
from graphene_django.filter.utils import replace_csv_filters

from django.db.models import Q, QuerySet
from functools import reduce


def get_filterset_class(filterset_class, **meta):
    """
    Get the class to be used as the FilterSet.
    """
    if filterset_class:
        # If were given a FilterSet class, then set it up.
        graphene_filterset_class = setup_filterset(filterset_class)
    else:
        # Otherwise create one.
        graphene_filterset_class = custom_filterset_factory(**meta)

    replace_csv_filters(graphene_filterset_class)

    return graphene_filterset_class


class GrapheneFilterSetMixin(BaseFilterSet):
    FILTER_DEFAULTS = FILTER_FOR_DBFIELD_DEFAULTS


def setup_filterset(filterset_class):
    """ Wrap a provided filterset in Graphene-specific functionality
    """
    return type(
        "Graphene{}".format(filterset_class.__name__),
        (filterset_class, GrapheneFilterSetMixin),
        {},
    )


def custom_filterset_factory(model, filterset_base_class=FilterSet, **meta):
    """
        Create a filterset for the given model using the provided meta data
    """
    meta.update({"model": model, "exclude": []})
    meta_class = type(str("Meta"), (object,), meta)
    filterset = type(
        str("%sFilterSet" % model._meta.object_name),
        (filterset_base_class, GrapheneFilterSetMixin),
        {"Meta": meta_class},
    )
    return filterset


class SearchFilterSetOptions(FilterSetOptions):
    def __init__(self, options=None):
        super().__init__(options)
        self.search_fields = getattr(options, "search_fields", None)


class SearchFilterSetMetaClass(FilterSetMetaclass):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        new_class._meta = SearchFilterSetOptions(
            getattr(new_class, "Meta", None))
        return new_class


class SearchFilterSet(BaseFilterSet, metaclass=SearchFilterSetMetaClass):
    search = CharFilter()

    def filter_queryset(self, queryset):
        qs = self.base_filter_queryset(queryset)
        if "search" in self.form.cleaned_data:
            search_fields = self._meta.search_fields
            search_value = self.form.cleaned_data["search"]
            list_of_Q = [Q(**{f'{key}__icontains': search_value})
                         for key in search_fields]
            qs = qs.filter(reduce(operator.or_, list_of_Q))
        return qs

    # same as BaseFilterSet but with the adition to exclude search field

    def base_filter_queryset(self, queryset):
        for name, value in self.form.cleaned_data.items():
            if name == "search":
                continue

            queryset = self.filters[name].filter(queryset, value)
            assert isinstance(queryset, QuerySet), \
                "Expected '%s.%s' to return a QuerySet, but got a %s instead." \
                % (type(self).__name__, name, type(queryset).__name__)
        return queryset
