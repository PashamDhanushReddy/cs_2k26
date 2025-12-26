from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('api/upload-ppt/', views.upload_ppt, name='upload_ppt'),
    path('api/submit-registration/', views.submit_registration, name='submit_registration'),
]
