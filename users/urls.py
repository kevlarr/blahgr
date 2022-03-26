from django.urls import path

from . import views

urlpatterns = [
    path('sign-up', views.signup, name='signup'),
    path('log-in', views.login, name='login'),
    path('log-out', views.logout, name='logout'),
]
