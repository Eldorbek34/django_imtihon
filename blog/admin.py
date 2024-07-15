from django.contrib import admin
from .models import Company, Product, Sale
from django.core.exceptions import ValidationError

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'qty', 'price')
    fields = ('title', 'company', 'qty', 'price')
    readonly_fields = ('company',)

    def delete_model(self, request, obj):
        if obj.qty > 0:
            raise ValidationError("Mahsulot soni 0 dan katta bo'lsa, uni o'chirib bo'lmaydi.")
        super().delete_model(request, obj)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'address', 'products_count')

    def delete_model(self, request, obj):
        if any(product.qty > 0 for product in obj.products.all()):
            raise ValidationError("Bu kompaniyada mahsulotlar mavjud, uni o'chirib bo'lmaydi.")
        super().delete_model(request, obj)

class SaleAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'product', 'quantity', 'sale_date')
    readonly_fields = ('customer_name', 'product', 'quantity', 'sale_date', 'sale_sum')
    fields = ('customer_name', 'product', 'quantity')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if obj.product.qty < obj.quantity:
            raise ValidationError("Mahsulot yetarli emas.")
        obj.product.qty -= obj.quantity
        obj.product.save()
        super().save_model(request, obj, form, change)

admin.site.register(Company, CompanyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)
