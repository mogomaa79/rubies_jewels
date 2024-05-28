from django.db import models

class Email(models.Model):
    email = models.EmailField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.email

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    images = models.ManyToManyField('ProductImage', related_name='products')

    def image_paths(self):
        return [str(img) for img in self.images.all()]

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(upload_to='store/static/images/products/', null=False, blank=False)

    def __str__(self):
        return self.image.url.split('/')[-1]
