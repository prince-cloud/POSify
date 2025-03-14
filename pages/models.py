from contextlib import nullcontext
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=600, default="no description")
    price = models.DecimalField(max_digits=100, decimal_places=2)
    available_quantity = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(blank=True, null=True)

    expected_sales = models.DecimalField(
        max_digits=100, decimal_places=2, null=True, blank=True
    )

    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = (
            "name",
            "-date",
        )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Product: {self.name[:10]}>"

    def save(self, *args, **kwargs):
        self.expected_sales = self.price * int(self.available_quantity)
        super(Product, self).save(*args, **kwargs)

    def is_expired(self):
        if self.expiry_date and (self.expiry_date < timezone.now().date()):
            return True
        return False


class Supply(models.Model):
    product = models.ForeignKey(
        Product, related_name="supplies", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def __repr__(self):
        return f"<Supply: {self.product.name} {self.quantity}>"

    def save(self, *args, **kwargs):
        self.product.available_quantity = int(self.product.available_quantity) + int(
            self.quantity
        )
        self.product.save()
        super(Supply, self).save(*args, **kwargs)


class Purchase(models.Model):
    customer = models.CharField(max_length=100, null=True, blank=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    date = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="sales"
    )

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return f"Purchase by {self.customer}"

    def __repr__(self):
        return f"<Purchase: GH{self.total_amount} by {self.CustomUsername}>"


class Expense(models.Model):
    description = models.CharField(max_length=600)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return self.description


class ItemPurchase(models.Model):
    product = models.ForeignKey(
        Product, related_name="purchases", on_delete=models.CASCADE
    )
    purchase = models.ForeignKey(
        Purchase, related_name="item_purchases", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField(auto_now_add=True)
    qty = models.PositiveIntegerField()
    seller = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="drugs_sold"
    )

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return f"Purchase of {self.quantity} {self.product.name}"

    def __repr__(self):
        return f"<ItemPurchase: {self.product.name} {self.quantity}>"

    def save(self, *args, **kwargs):
        self.qty = self.product.available_quantity
        self.product.available_quantity = int(self.product.available_quantity) - int(
            self.quantity
        )
        self.qty = self.product.available_quantity
        self.product.save()
        super(ItemPurchase, self).save(*args, **kwargs)
