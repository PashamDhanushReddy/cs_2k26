from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_team, name='register'),
    path('register', views.register_team),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('registration-success', views.registration_success),
]
