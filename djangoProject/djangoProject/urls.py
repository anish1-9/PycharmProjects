from django.urls import path, include
from django.contrib import admin
from . import views  # Uncommented this line

urlpatterns = [
    path('', views.index, name='index'),
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),  # Added closing parenthesis
]





