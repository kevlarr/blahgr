from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='blog-index'),
    path('new/', views.new, name='blog-new'),
    path('<int:post_id>/', views.details, name='blog-details'),
]
