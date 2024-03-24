from web import models
from django import forms
from utils.bootstrapclass import Bootstrap


class PriceForm(Bootstrap, forms.ModelForm):
    class Meta:
        model = models.PricePolicy
        fields = '__all__'
