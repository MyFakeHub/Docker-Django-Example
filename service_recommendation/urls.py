from django.urls import path
from . import views

app_name = 'service_recommendation'
urlpatterns = [
    path('', views.index, name='index'),
    path('random/', views.random, name='random')
]