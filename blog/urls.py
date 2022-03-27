from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='blog-index'),
    path('new/', views.new, name='blog-new'),
    path('<int:post_id>/', views.details, name='blog-details'),
    path('<int:post_id>/delete', views.delete, name='blog-delete'),
    path('<int:post_id>/comments/new', views.new_comment, name='comment-new'),
    path('comments/<int:comment_id>/delete', views.delete_comment, name='comment-delete'),
]
