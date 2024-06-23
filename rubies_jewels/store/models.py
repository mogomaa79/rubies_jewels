from django.db import models
from django.db.models import Q
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
import uuid


class Email(models.Model):
    email = models.EmailField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.email

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.TextField(max_length=500, null=False, blank=False)
    material = models.CharField(max_length=100, null=False, blank=False)
    stock = models.IntegerField(null=False, blank=False)
    images = models.ManyToManyField('Image', through='ProductImageRelation')

    def main_image(self):
        relation = self.productimagerelation_set.filter(is_main=True).first()
        return relation.image if relation else None

    def images(self):
        return [rel.image for rel in self.productimagerelation_set.all()]

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    image = CloudinaryField('image')

    def __str__(self):
        return self.name


class ProductImageRelation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False, unique=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'is_main'],
                condition=Q(is_main=True),
                name='unique_main_image'
            )
        ]
    
    def __str__(self):
        return f"{self.product} ({self.image}){' (MAIN)' if self.is_main else ''}"

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    image1 = models.ForeignKey(Image, related_name='image1', on_delete=models.CASCADE)
    image2 = models.ForeignKey(Image, related_name='image2', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(uuid.uuid4())
        super(User, self).save(*args, **kwargs)

class Offer(models.Model):
    id = models.AutoField(primary_key=True)
    product1 = models.ForeignKey('Product', related_name='bundle_offer1', on_delete=models.CASCADE)
    product2 = models.ForeignKey('Product', related_name='bundle_offer2', on_delete=models.CASCADE)
    bundle_price = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    
    @property
    def old_price(self):
        return self.product1.price + self.product2.price

    def __str__(self):
        return f"Bundle Offer: {self.product1.name} + {self.product2.name}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    @property
    def coupon_discount(self):
        return self.total_price * (self.coupon.discount / 100)  if self.coupon else 0

    @property
    def total_price_after_discount(self):
        return self.total_price - self.coupon_discount if self.coupon else self.total_price


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.product:
            return f"{self.quantity} of {self.product.name}"
        else:
            return f"{self.quantity} of {self.offer.product1.name} and {self.offer.product2.name} offer"

    @property
    def total_price(self):
        if self.product:
            return self.quantity * self.product.price
        elif self.offer:
            return self.quantity * self.offer.bundle_price


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.code} ({self.discount}%)"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    deliver = models.BooleanField(default=False)

    def __str__(self):
        return f"Order by {self.user.first_name} {self.user.last_name} on {self.date.date()}, {self.date.hour}:{self.date.minute} {'(DELIVERED)' if self.delivered else ''}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.product:
            return f"{self.quantity} of {self.product.name} in order {self.order.id}"
        else:
            return f"{self.quantity} of {self.offer.product1.name} and {self.offer.product2.name} offer in order {self.order.id}"

    @property
    def subtotal(self):
        if self.product:
            return self.quantity * self.product.price
        else:
            return self.quantity * self.offer.bundle_price

