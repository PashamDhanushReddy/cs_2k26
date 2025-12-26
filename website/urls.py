from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.idea_register, name='idea_register'),
    path('csrf-debug/', views.csrf_debug, name='csrf_debug'),
]
