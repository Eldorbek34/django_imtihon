from django.db import models
from django.core.exceptions import ValidationError

class Company(models.Model):
    title = models.CharField("Kompaniya nomi", max_length=250)
    phone = models.CharField("Tel raqami", max_length=20)
    address = models.TextField("lakatsiya")

    @property
    def products_count(self):
        return self.products.count()

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if any(product.qty > 0 for product in self.products.all()):
            raise ValidationError("Ushbu kompaniyada mahsulotlar mavjud,  o'chirib bo'lmaydi.")
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Kompaniyalar"
        verbose_name = "kompaniya"

class Product(models.Model):
    title = models.CharField("Mahsulot nomi", max_length=250)
    price = models.IntegerField("Narxi")
    qty = models.IntegerField("Mahsulot soni", default=0)
    company = models.ForeignKey('Company', related_name='products', verbose_name='Kompaniya', on_delete=models.CASCADE)

    def clean(self):
        if self.qty < 0:
            raise ValidationError("Kechirasiz butun son kriting")
        if self.price < 0:
            raise ValidationError("Kechirasiz butun son kriting")

    def __str__(self):
        return f"{self.title} ({self.company})"

    def delete(self, *args, **kwargs):
        if self.qty > 0:
            raise ValidationError("Mahsulot soni 0 dan katta bo'lsa, uni o'chirib bo'lmaydi.")
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Mahsulotlar"
        verbose_name = "mahsulot"

class Sale(models.Model):
    customer_name = models.CharField("Haridorning nomi", max_length=255, default='Olim mani ismim')
    product = models.ForeignKey(Product, verbose_name='Mahsulot', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField("Mahsulot soni")
    sale_date = models.DateTimeField("Sana", auto_now_add=True)

    @property
    def sale_sum(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.customer_name}ga {self.product.title} mahsuloti sotuvi'

    def save(self, *args, **kwargs):
        if self.product.qty < self.quantity:
            raise ValidationError("Mahsulot yetarli emas.")
        self.product.qty -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Savdolar"
        verbose_name = "savdo"
