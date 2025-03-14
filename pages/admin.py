from django.contrib import admin
from .models import Product, Purchase, ItemPurchase, Expense
from unfold.admin import ModelAdmin

# Register your models here.


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        "name",
        "price",
        "available_quantity",
        "description",
        "expected_sales",
    )
    search_fields = ("name", "description")


@admin.register(Expense)
class ExpenseAdmin(ModelAdmin):
    list_display = ("date", "description", "amount")


@admin.register(Purchase)
class PurchaseAdmin(ModelAdmin):
    list_display = ("customer", "total_amount", "date", "seller")


@admin.register(ItemPurchase)
class ItemPurchaseAdmin(ModelAdmin):
    list_display = ("product", "quantity", "total_amount", "date", "seller")
