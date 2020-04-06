from django.db import models

class CanalYT(models.Model):
    titulo = models.CharField(max_length=64)
    link = models.CharField(max_length=64)

class Video(models.Model):
    canal = models.ForeignKey(CanalYT, on_delete=models.CASCADE, null = True)
    titulo = models.CharField(max_length=64, null = True)
    link = models.CharField(max_length=64, null = True)
    esta_seleccionado = models.BooleanField(default = False)
    ytid = models.CharField(max_length=64, null = True)
    img = models.CharField(max_length=128, null = True)
    fechaPub = models.DateTimeField('publicado', null = True)
    descri = models.CharField(max_length=256, null = True)
    def __str__(self):
        return self.titulo
