from django.forms import ModelForm      
from .models import Image

class PhotoForm(ModelForm):
  class Meta:
      model = Image
      fields = ['image']