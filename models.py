from django.db import models

# Create your models here.

class searchWeather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    pressure = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"{self.city} at {self.date.strftime('%Y-%m-%d %H:%M')}"