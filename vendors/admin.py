from django.contrib import admin
from vendors.models import Franchise, FranchiseOrder, menubuilding, multivendors
# Register your models here.


@admin.register(multivendors)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("restaurant_name", "user", "city", "state", "is_approved", "Franchise")
    list_filter = ("is_approved", "Franchise", "city", "state")
    search_fields = ("restaurant_name", "user__username", "city")


@admin.register(menubuilding)
class MenuBuildingAdmin(admin.ModelAdmin):
    list_display = ("food_name", "ver", "price")
    list_filter = ("ver",)
    search_fields = ("food_name", "ver__restaurant_name")


@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    list_display = ("vendor", "total_investment", "total_year_of_aggr", "profit_share")
    search_fields = ("vendor__restaurant_name",)


@admin.register(FranchiseOrder)
class FranchiseOrderAdmin(admin.ModelAdmin):
    list_display = ("user", "vendor", "franchise", "created_at")
    list_filter = ("vendor", "created_at")
    search_fields = ("user__username", "vendor__restaurant_name")
