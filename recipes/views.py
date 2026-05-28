import requests
from decouple import config
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from .models import FavoriteRecipe

TMDB_KEY = config('THEMEALDB_API_KEY', default='1')
BASE_URL = f'https://www.themealdb.com/api/json/v1/{TMDB_KEY}'

POPULAR_AREAS = [
    'Italian', 'Mexican', 'Japanese', 'Chinese', 'Thai',
    'Greek', 'Spanish', 'Portuguese', 'British', 'Turkish',
    'Vietnamese', 'Moroccan', 'Polish', 'Russian', 'Jamaican',
    'Egyptian', 'Filipino',
]


def _build_ingredients(meal):
    """TheMealDB devolve strIngredient1..20 + strMeasure1..20.
    Combina em uma lista de dicts {ingredient, measure} ignorando vazios."""
    items = []
    for i in range(1, 21):
        ing = (meal.get(f'strIngredient{i}') or '').strip()
        meas = (meal.get(f'strMeasure{i}') or '').strip()
        if ing:
            items.append({'ingredient': ing, 'measure': meas})
    return items


def _youtube_embed(url):
    """Converte URL do YouTube em URL embed nocookie (ou retorna None).
    Usa o domínio youtube-nocookie.com porque funciona com mais vídeos restritos."""
    if not url or 'watch?v=' not in url:
        return None
    video_id = url.split('watch?v=')[1].split('&')[0]
    return f'https://www.youtube-nocookie.com/embed/{video_id}'


def home(request):
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()
    area_filter = request.GET.get('area', '').strip()

    if query:
        data = requests.get(f'{BASE_URL}/search.php', params={'s': query}).json()
        meals = data.get('meals') or []
    elif area_filter:
        data = requests.get(f'{BASE_URL}/filter.php', params={'a': area_filter}).json()
        meals = data.get('meals') or []
    elif category_filter:
        data = requests.get(f'{BASE_URL}/filter.php', params={'c': category_filter}).json()
        meals = data.get('meals') or []
    else:
        data = requests.get(f'{BASE_URL}/filter.php', params={'c': 'Beef'}).json()
        meals = data.get('meals') or []
        category_filter = 'Beef'

    categories = requests.get(f'{BASE_URL}/categories.php').json().get('categories', [])

    paginator = Paginator(meals, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/home.html', {
        'page_obj': page_obj,
        'query': query,
        'category_filter': category_filter,
        'area_filter': area_filter,
        'categories': categories,
        'areas': POPULAR_AREAS,
    })


def recipe_detail(request, meal_id):
    data = requests.get(f'{BASE_URL}/lookup.php', params={'i': meal_id}).json()
    meal = data['meals'][0]
    ingredients = _build_ingredients(meal)
    youtube_embed = _youtube_embed(meal.get('strYoutube'))

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = FavoriteRecipe.objects.filter(
            user=request.user, meal_id=meal_id,
        ).exists()

    return render(request, 'recipes/recipe_detail.html', {
        'meal': meal,
        'ingredients': ingredients,
        'youtube_embed': youtube_embed,
        'is_favorited': is_favorited,
    })


def random_recipe(request):
    data = requests.get(f'{BASE_URL}/random.php').json()
    meal = data['meals'][0]
    ingredients = _build_ingredients(meal)
    youtube_embed = _youtube_embed(meal.get('strYoutube'))

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = FavoriteRecipe.objects.filter(
            user=request.user, meal_id=meal['idMeal'],
        ).exists()

    return render(request, 'recipes/recipe_detail.html', {
        'meal': meal,
        'ingredients': ingredients,
        'youtube_embed': youtube_embed,
        'is_favorited': is_favorited,
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso! Bem-vindo(a) ao Food Explorer.')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def add_favorite(request, meal_id):
    data = requests.get(f'{BASE_URL}/lookup.php', params={'i': meal_id}).json()
    meal = (data.get('meals') or [None])[0]
    if not meal:
        messages.error(request, 'Receita não encontrada.')
        return redirect('home')

    _, created = FavoriteRecipe.objects.get_or_create(
        user=request.user,
        meal_id=meal_id,
        defaults={
            'title': meal['strMeal'],
            'thumb': meal.get('strMealThumb', ''),
            'category': meal.get('strCategory', ''),
        },
    )
    if created:
        messages.success(request, f'"{meal["strMeal"]}" adicionada aos favoritos!')
    else:
        messages.info(request, 'Essa receita já está nos seus favoritos.')
    return redirect('recipe_detail', meal_id=meal_id)


@login_required
def favorites(request):
    items = FavoriteRecipe.objects.filter(user=request.user)
    return render(request, 'recipes/favorites.html', {'favorites': items})


@login_required
def remove_favorite(request, meal_id):
    deleted, _ = FavoriteRecipe.objects.filter(
        user=request.user, meal_id=meal_id,
    ).delete()
    if deleted:
        messages.success(request, 'Receita removida dos favoritos.')
    return redirect('favorites')

@login_required
def shopping_list(request):
    favorites = FavoriteRecipe.objects.filter(user=request.user)

    shopping = {}
    for fav in favorites:
        data = requests.get(f'{BASE_URL}/lookup.php', params={'i': fav.meal_id}).json()
        meal = (data.get('meals') or [None])[0]
        if not meal:
            continue
        for item in _build_ingredients(meal):
            ing = item['ingredient']
            if ing not in shopping:
                shopping[ing] = []
            shopping[ing].append({
                'measure': item['measure'],
                'recipe_title': fav.title,
            })

    shopping_sorted = dict(sorted(shopping.items()))

    return render(request, 'recipes/shopping_list.html', {
        'shopping': shopping_sorted,
        'recipe_count': favorites.count(),
    })