from django.urls import path
from . import views
# from auth import urls

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('error', views.error, name='error'),
    path('electionSetting', views.electionSetting, name='electionSetting'),
    path('myAccount', views.myAccount, name='myAccount'),
    path('dashboard', views.candidateDB, name='candidateDB'),
    path('ecDB', views.ecDB, name='ecDB'),
    path('voterDB', views.voterDB, name='voterDB'),
    path('update', views.updateProfile, name='update'),
]