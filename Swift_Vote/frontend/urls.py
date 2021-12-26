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
    path('candidateApplication', views.candidateApplication, name="candidateApplication"),
    path('cResults', views.cResults, name='cResults'),
    path('vResults', views.vResults, name='vResults'),
    path('ecDB', views.ecDB, name='ecDB'),
    path('logout', views.logout),
    path('voterDB', views.voterDB, name='voterDB'),
    path('update', views.updateProfile, name='update'),
    path('createElection', views.createElection, name='createElection'),
    path('disableElection', views.disableElection, name='disableElection'),
    path('electionHistory', views.electionHistory, name='electionHistory'),
    path('ack', views.ack, name='ack'),
    path('voting', views.voting, name='voting'),
]
