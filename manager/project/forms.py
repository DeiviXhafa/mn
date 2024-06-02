from django import forms
from django.apps import apps
def create_model_form(model_object):
    class Meta:
        model = model_object
        fields = '__all__'
    attrs = {'Meta': Meta}
    return type(f'{model_object.__name__}Form', (forms.ModelForm,), attrs)
