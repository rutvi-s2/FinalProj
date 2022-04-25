# forms.py 
from django import forms 
from .models import User_Image

class User_Image_Form(forms.ModelForm): 
    class Meta: 
        model = User_Image
        fields = ['profile_image'] 