from django.contrib import admin
from .models import *
from cloudinary.forms import CloudinaryFileField
from django import forms

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImageRelation)


class ImageAdminForm(forms.ModelForm):
    image = CloudinaryFileField(
        options={
            'folder': 'rubies_jewels/products',
            'resource_type': 'auto',
            'overwrite': True,
        }
    )

    class Meta:
        model = Image
        fields = '__all__'

class ImageAdmin(admin.ModelAdmin):
    form = ImageAdminForm

admin.site.register(Image, ImageAdmin)
admin.site.register(User)
admin.site.register(Coupon)
admin.site.register(OrderItem)
admin.site.register(Cart)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)