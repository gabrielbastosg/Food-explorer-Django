from .models import FavoriteRecipe


def favorite_count(request):
    if request.user.is_authenticated:
        count = FavoriteRecipe.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'favorite_count': count}
