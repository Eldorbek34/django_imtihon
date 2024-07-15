from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone



class Company(models.Model):
    title = models.CharField("Company title", max_length=250)
    phone = models.CharField("Company phone", max_length=50)
    address = models.CharField("Company address", max_length=250)

    class Meta:
        verbose_name_plural = "Kompaniyalar"
        verbose_name = "Kompaniya"

    def str(self):
        return self.title

    def products_type(self):
        return self.product_set.count()

    products_type.short_description = "Mahsulot turi"


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    class Meta:
        verbose_name_plural = "Xaridorlar"

    def str(self):
        return self.name
class Product(models.Model):
    title = models.CharField("Mahsulot nomi", max_length=250)
    price = models.IntegerField("Narxi",)
    qty = models.IntegerField("Mahsulot soni",default=0)
    company = models.ForeignKey('blog.Company', verbose_name='Kompaniya', on_delete=models.CASCADE)

    def clean(self):
        if self.qty < 0:
            raise ValidationError("Manfiy son kiritsh mumkin emas")
        if self.price < 0:
            raise ValidationError("Manfiy son kiritsh mumkin emas")

    def str(self):
        return f"{self.title} {self.company}"

    class Meta:
        verbose_name_plural = "Mahsulotlar"
        verbose_name = "mahsulot"



class Sale(models.Model):
    customer = models.ForeignKey('blog.Customer', verbose_name='Xaridor', on_delete=models.CASCADE)
    product = models.ForeignKey('blog.Product', verbose_name='Mahsulot', on_delete=models.CASCADE)
    company = models.ForeignKey('blog.Company', verbose_name='Kompaniya' ,on_delete=models.CASCADE)
    quantity_sold = models.IntegerField(verbose_name='Sotilgan soni')
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name='Sotilgan vaqti')

    class Meta:
        verbose_name_plural = "Savdolar"
        verbose_name = "Savdo"

    def total_amount(self):
        return self.product.price * self.quantity_sold

    total_amount.short_description = "Umumiy narxi"

    def clean(self):
        if self.quantity_sold < 0:
            raise ValidationError('Sotilgan soni manfiy bo\'lmasligi kerak.')

    def save(self, *args, **kwargs):
        self.clean()
        if self.product.company != self.company:
            raise ValidationError('Selected product does not belong to the selected company.')

        if self.product.qty >= self.quantity_sold:
            self.product.qty -= self.quantity_sold
            self.product.save()
            super().save(*args, **kwargs)
        else:
            raise ValueError('Mahsulot soni yetarli emas!')

    def str(self):
        return f'{self.customer.name} - {self.product.title} - {self.quantity_sold}'