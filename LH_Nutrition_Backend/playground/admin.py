from django.contrib import admin
from .models import Article

# Register your models here.
@admin.register(Article)

class ArticleModel(admin.ModelAdmin):
    list_filter = ('title','calories','protein','count','meal','servingSize', 'diningHall','sodium','fat','chol','carbs','sugar','line')
    list_display = ('title','calories','protein','count','meal','servingSize', 'diningHall','sodium','fat','chol','carbs','sugar','line')