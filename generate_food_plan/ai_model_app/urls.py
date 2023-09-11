from django.urls import path
from .views import generate_plan


urlpatterns = [
    path('generate_plan/', generate_plan, name='generate_plan'),
]