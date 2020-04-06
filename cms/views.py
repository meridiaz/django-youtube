from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404

from .models import Video


@csrf_exempt
def index(request):
    videos_list = Video.objects.all()
    context = {'videos_list': videos_list}
    if request.method == "POST":
        video_id = request.POST['action']
        v = Video.objects.get(ytid=video_id)
        v.esta_seleccionado = not v.esta_seleccionado
        v.save()
    return render(request, 'cms/index.html', context)


@csrf_exempt
def get_content(request, llave):
    v = get_object_or_404(Video, ytid=llave)
    context = {'video': v}
    return render(request, 'cms/video.html', context)
