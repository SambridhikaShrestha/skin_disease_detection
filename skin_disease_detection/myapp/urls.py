from django.urls import path
from .views import home, root

urlpatterns = [
    path("home/", home),
    path("", root)
]
