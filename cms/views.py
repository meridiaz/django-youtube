from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Contenido

@csrf_exempt
def get_content(request, llave):
    if request.method == "PUT":
        valor = request.body.decode('utf-8')
        try:
            respuesta = Contenido.objects.get(clave=llave).valor
            #si ya existe esa llave la sustituyo por el nuevo valor
            valor2 = Contenido.objects.get(clave=llave)
            valor2.valor = valor
            valor2.save()
        except Contenido.DoesNotExist:
            c = Contenido(clave=llave, valor=valor)
            c.save()
        return HttpResponse('<h1>Valor añadidio con exito</h1>')
        
    elif request.method == "GET":
        try:
            respuesta = Contenido.objects.get(clave=llave).valor
        except Contenido.DoesNotExist:
            respuesta = "No existe contenido para la clave: " +llave
        return HttpResponse(respuesta)
