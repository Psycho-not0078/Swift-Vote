from django.urls import path
from . import views
# from auth import urls

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('error', views.error, name='error'),
    path('register', views.register, name='register'),
]