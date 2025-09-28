# kitchen/forms.py
from django import forms
from .models import Dish, DishType, Cook


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ("name", "dish_type", "description", "price", "cooks")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "cooks": forms.CheckboxSelectMultiple,
        }


class DishTypeForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = ("name", "description")
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class CookForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = ("first_name", "last_name", "years_of_experience")
