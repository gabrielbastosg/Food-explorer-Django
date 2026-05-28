from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<str:meal_id>/', views.recipe_detail, name='recipe_detail'),
    path('register/', views.register, name='register'),
    path('favorite/<str:meal_id>/', views.add_favorite, name='add_favorite'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorite/remove/<str:meal_id>/', views.remove_favorite, name='remove_favorite'),
    path('random/', views.random_recipe, name='random_recipe'),
    path('shopping-list/', views.shopping_list, name='shopping_list'),
]
