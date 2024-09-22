from django.db import models

# Create your models here.

class Pessoa(models.Model):
    nome = models.CharField(max_length = 50)
    sobrenome = models.CharField(max_length = 50)
    data_nascimento = models.DateTimeField()

    def __str__(self):
        return self.nome