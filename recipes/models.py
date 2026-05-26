from django.db import models
from django.contrib.auth.models import User


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_recipes')
    meal_id = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    thumb = models.URLField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'meal_id')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.title}'
