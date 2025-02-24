from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=100, default='N/A')
    calories = models.IntegerField()
    protein = models.DecimalField(decimal_places=1,max_digits=5,default=0.0) 
    count = models.JSONField(default=dict)
    meal = models.IntegerField(default=1)
    servingSize = models.TextField(max_length=100, default='N/A')
    diningHall = models.IntegerField(default=1)
    sodium = models.DecimalField(decimal_places=1,max_digits=5,default=0.0) 
    fat = models.DecimalField(decimal_places=1,max_digits=5,default=0.0) 
    chol = models.DecimalField(decimal_places=1,max_digits=5,default=0.0) 
    carbs = models.DecimalField(decimal_places=1,max_digits=5,default=0.0) 
    sugar = models.DecimalField(decimal_places=1,max_digits=5,default=0.0) 
    line = models.TextField(max_length=100, default='N/A')



    def __str__(self):
        return self.title
