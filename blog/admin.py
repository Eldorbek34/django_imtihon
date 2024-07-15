from django.contrib import admin
from .models import Product, Company, Sale, Customer

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'price', 'qty', 'company')
    fields = ('title', 'company', 'qty', 'price')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['company']
        else:
            return []

    def has_delete_permission(self, request, obj=None):
        if obj and obj.qty > 0:
            return False
        return True

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'address', 'products_type', 'get_total_qty')

    def has_delete_permission(self, request, obj=None):
        if obj and any(product.qty > 0 for product in obj.product_set.all()):
            return False
        return super().has_delete_permission(request, obj)

    def get_total_qty(self, obj):
        products = Product.objects.filter(company=obj)
        total_qty = sum(product.qty for product in products)
        return total_qty

    get_total_qty.short_description = "Mahsulot soni"

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('customer', 'company', 'product', 'quantity_sold', 'total_amount', 'sale_date')

    def total_amount(self, obj):
        return obj.total_amount

    total_amount.short_description = "Umumiy narxi"

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',)
