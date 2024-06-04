from django.db import models
from django.db.models import Q


class Email(models.Model):
    email = models.EmailField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.email

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    material = models.CharField(max_length=100, null=False, blank=False)
    stock = models.IntegerField(null=False, blank=False)
    insta_link = models.URLField(null=False, blank=False)
    images = models.ManyToManyField('ProductImage', through='ProductImageRelation')

    def main_image(self):
        relation = self.productimagerelation_set.filter(is_main=True).first()
        return relation.image if relation else None

    def image_paths(self):
        return [str(assoc.image) for assoc in self.productimagerelation_set.all()]

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='store/static/images/products/', null=False, blank=False)

    def __str__(self):
        return self.image.url.split('/')[-1]


class ProductImageRelation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(ProductImage, on_delete=models.CASCADE)
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

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=15, null=False, blank=False)
    address = models.TextField(max_length=500, null=False, blank=False)
    orders = models.ManyToManyField('Order', related_name='users')


    def __str__(self):
        return self.name
    

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    products = models.ManyToManyField('Product', related_name='orders')
    quantity = models.IntegerField(null=False, blank=False)
    total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.product.name