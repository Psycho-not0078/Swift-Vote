from django.urls import path
from . import views
# from auth import urls

urlpatterns = [
    path('login/', views.login, name='login'),
    path('error', views.error, name='error'),
]