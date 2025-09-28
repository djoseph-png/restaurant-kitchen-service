from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import CookForm, DishForm, DishTypeForm
from .models import Cook, Dish, DishType


class HomeView(TemplateView):
    template_name = "kitchen/home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["dish_count"] = Dish.objects.count()
        ctx["type_count"] = DishType.objects.count()
        ctx["cook_count"] = Cook.objects.count()
        ctx["top_types"] = (
            DishType.objects.annotate(total=Count("dishes"))
            .order_by("-total", "name")[:5]
        )
        return ctx


# ---------- Dish ----------
class DishListView(ListView):
    model = Dish
    paginate_by = 10
    context_object_name = "dish_list"
    template_name = "kitchen/dish_list.html"

    def get_queryset(self):
        qs = (
            Dish.objects.select_related("dish_type")
            .prefetch_related("cooks")
            .order_by("name")
        )
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q)
                | Q(description__icontains=q)
                | Q(dish_type__name__icontains=q)
                | Q(cooks__first_name__icontains=q)
                | Q(cooks__last_name__icontains=q)
            ).distinct()
        return qs


class DishDetailView(DetailView):
    model = Dish
    context_object_name = "dish"
    template_name = "kitchen/dish_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["all_cooks"] = Cook.objects.order_by("last_name", "first_name")
        return ctx


class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish_form.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish_form.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, DeleteView):
    model = Dish
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-list")


class ToggleCookForDishView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        dish = get_object_or_404(Dish, pk=pk)
        cook_id = request.POST.get("cook_id")
        cook = get_object_or_404(Cook, pk=cook_id)
        if cook in dish.cooks.all():
            dish.cooks.remove(cook)
            messages.success(request, "Cozinheiro removido do prato.")
        else:
            dish.cooks.add(cook)
            messages.success(request, "Cozinheiro atribuído ao prato.")
        return redirect("kitchen:dish-detail", pk=pk)


# ---------- DishType ----------
class DishTypeListView(ListView):
    model = DishType
    paginate_by = 10
    context_object_name = "dishtype_list"
    template_name = "kitchen/dishtype_list.html"

    def get_queryset(self):
        qs = DishType.objects.order_by("name")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return qs


class DishTypeDetailView(DetailView):
    model = DishType
    context_object_name = "dishtype"
    template_name = "kitchen/dishtype_detail.html"


class DishTypeCreateView(LoginRequiredMixin, CreateView):
    model = DishType
    form_class = DishTypeForm
    template_name = "kitchen/dishtype_form.html"
    success_url = reverse_lazy("kitchen:dishtype-list")


class DishTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = DishType
    form_class = DishTypeForm
    template_name = "kitchen/dishtype_form.html"
    success_url = reverse_lazy("kitchen:dishtype-list")


class DishTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = DishType
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:dishtype-list")


# ---------- Cook ----------
class CookListView(ListView):
    model = Cook
    paginate_by = 10
    context_object_name = "cook_list"
    template_name = "kitchen/cook_list.html"

    def get_queryset(self):
        qs = Cook.objects.order_by("last_name", "first_name")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(dishes__name__icontains=q)
            ).distinct()
        return qs


class CookDetailView(DetailView):
    model = Cook
    context_object_name = "cook"
    template_name = "kitchen/cook_detail.html"


class CookCreateView(LoginRequiredMixin, CreateView):
    model = Cook
    form_class = CookForm
    template_name = "kitchen/cook_form.html"
    success_url = reverse_lazy("kitchen:cook-list")


class CookUpdateView(LoginRequiredMixin, UpdateView):
    model = Cook
    form_class = CookForm
    template_name = "kitchen/cook_form.html"
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(LoginRequiredMixin, DeleteView):
    model = Cook
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:cook-list")
