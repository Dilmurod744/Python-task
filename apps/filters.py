from django.contrib import admin
from django.contrib.admin import SimpleListFilter


class PriceRangeFilter(SimpleListFilter):
    title = "Price range"
    parameter_name = "price_range"

    def lookups(self, request, model_admin):
        return (
            ("0-1000", "0 - 1000"),
            ("1000-5000", "1000 - 5000"),
            ("5000-10000", "10000 - 100000"),
            ("100000-", "100000+"),
        )

    def queryset(self, request, queryset):
        if self.value() == "0-1000":
            return queryset.filter(price__range=(0, 1000))
        elif self.value() == "1000-5000":
            return queryset.filter(price__range=(1000, 5000))
        elif self.value() == "5000-10000":
            return queryset.filter(price__range=(5000, 10000))
        elif self.value() == "100000-":
            return queryset.filter(price__gte=1000)
