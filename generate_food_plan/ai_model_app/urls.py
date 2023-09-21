from django.urls import path
from . import views


urlpatterns = [
    path('', views.home , name='home'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('generate_plan/', views.generate_plan, name='generate_plan'),
]