# kitchen/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),

    # Dish
    path("dishes/", views.DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", views.DishDetailView.as_view(), name="dish-detail"),
    path("dishes/create/", views.DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/update/", views.DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/", views.DishDeleteView.as_view(), name="dish-delete"),

    # DishType
    path("types/", views.DishTypeListView.as_view(), name="dishtype-list"),
    path("types/<int:pk>/", views.DishTypeDetailView.as_view(), name="dishtype-detail"),
    path("types/create/", views.DishTypeCreateView.as_view(), name="dishtype-create"),
    path(
        "types/<int:pk>/update/",
        views.DishTypeUpdateView.as_view(),
        name="dishtype-update",
    ),
    path(
        "types/<int:pk>/delete/",
        views.DishTypeDeleteView.as_view(),
        name="dishtype-delete",
    ),

    # Cook
    path("cooks/", views.CookListView.as_view(), name="cook-list"),
    path("cooks/<int:pk>/", views.CookDetailView.as_view(), name="cook-detail"),
    path("cooks/create/", views.CookCreateView.as_view(), name="cook-create"),
    path("cooks/<int:pk>/update/", views.CookUpdateView.as_view(), name="cook-update"),
    path("cooks/<int:pk>/delete/", views.CookDeleteView.as_view(), name="cook-delete"),

    # Atribuir/Remover cook em Dish (toggle via POST)
    path(
        "dishes/<int:pk>/toggle-cook/",
        views.ToggleCookForDishView.as_view(),
        name="dish-toggle-cook",
    ),
]
