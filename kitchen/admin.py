from django.contrib import admin
from .models import DishType, Cook, Dish, Ingredient


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Cook)
class CookAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "years_of_experience")
    search_fields = ("first_name", "last_name")


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "dish_type", "price")
    list_filter = ("dish_type",)
    search_fields = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "unit")
    search_fields = ("name",)
