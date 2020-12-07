import django_filters
from images.models import Pictures
from django.db import models
from django.db.models.functions import Lower

class TagsFilter(django_filters.FilterSet):

    category  = django_filters.AllValuesFilter( widget=django_filters.widgets.LinkWidget(), field_name="category", label="Category")
    
    class Meta:
        model = Pictures
        fields = ['tags__name']
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'iexact',
                },
            }
        
        }

class CategoryFilter(django_filters.FilterSet):

    category  = django_filters.AllValuesFilter( widget=django_filters.widgets.LinkWidget(), field_name="category", label="Category")

    class Meta:
        model = Pictures
        fields = ['category']