from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    release_date = models.DateField(null=True)
    genre = models.CharField(max_length=255,null=True)
    # poster = models.URLField()

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    comment = models.TextField(null=True)

    def __str__(self):
        return f"{self.movie.title} - {self.user.username}"