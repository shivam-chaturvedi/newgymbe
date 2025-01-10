from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)  
    password = models.CharField(max_length=200)  

    def __str__(self):
        return self.name
