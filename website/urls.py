from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.idea_register, name='idea_register'),
]
