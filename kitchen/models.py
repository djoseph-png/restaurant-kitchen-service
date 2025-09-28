from django.conf import settings
from django.db import models


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Cook(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cook_profile",
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    years_of_experience = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    dish_type = models.ForeignKey(
        DishType, on_delete=models.PROTECT, related_name="dishes"
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cooks = models.ManyToManyField(Cook, related_name="dishes", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


# Opcional recomendado
class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    unit = models.CharField(max_length=32, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


# Campo N:N opcional (adicione em Dish se for usar Ingredient)
#   ingredients = models.ManyToManyField(Ingredient, related_name="dishes", blank=True)
