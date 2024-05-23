from django.db import models

class Email(models.Model):
    email = models.EmailField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.email

class Item(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    image_url = models.URLField(null=False, blank=False)
    stock = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name