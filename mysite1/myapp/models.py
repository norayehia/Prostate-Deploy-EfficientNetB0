from django.db import models

# Create your models here.
from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    prediction = models.IntegerField()

    def __str__(self):
        return f"Image: {self.image}, Prediction: {self.prediction}"