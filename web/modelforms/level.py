from web import models
from django import forms

from utils.bootstrapclass import Bootstrap


class LevelModelForm(Bootstrap, forms.ModelForm):
    class Meta:
        model = models.Level
        fields = ['title', 'percent']
