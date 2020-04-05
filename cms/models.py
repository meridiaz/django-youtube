from django.db import models

class Video(models.Model):
    titulo = models.CharField(max_length=64)
    link = models.CharField(max_length=64)
    esta_seleccionado = models.BooleanField(default = False)
    def __str__(self):
        return self.titulo
