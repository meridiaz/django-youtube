from django.urls import path

from . import views

urlpatterns = [
    path('<str:llave>', views.get_content),
]
