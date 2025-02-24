from rest_framework import serializers
from .models import Article




class ArticleSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Article
        fields = ['id', 'title', 'calories', 'protein', 'count', 'meal','servingSize','diningHall', 'sodium','fat','chol','carbs','sugar','line']

'''
def create(self, validated_data):
    return Article.objects.create(validated_data)


def update(self, instance, validated_data):
    instance.title = validated_data.get('title', instance.title)
    instance.calories = validated_data.get('calories', instance.calories)
    instance.protein = validated_data.get('protein', instance.protein) '''