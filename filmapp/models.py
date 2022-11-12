from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Actor(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=40, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    birth_year = models.DateField(null=True, blank=True)
    def __str__(self) -> str:
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, blank=True)
    year = models.DateField(null=True, blank=True)
    rating = models.FloatField(blank=True, null=True)
    actors = models.ManyToManyField(Actor, blank=True)
    def __str__(self) -> str:
        return self.name

class Comment(models.Model):
    note = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    def __str__(self) -> str:
        return f"{self.movie} comments"