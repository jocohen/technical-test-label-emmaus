from django.urls import path

from main import views

app_name = "main"

urlpatterns = [path("", views.NasaView.as_view(), name="nasa")]
