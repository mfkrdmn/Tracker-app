from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('addexpense', views.addexpense, name = 'addexpense'),

]
