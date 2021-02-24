from djongo import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Plays(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Videos(models.Model):
    title = models.CharField(max_length=100)
    play = models.CharField(max_length=100)
    rend = models.CharField(max_length=10)
    video = models.FileField(blank=False)