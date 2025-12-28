from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('create-post/', views.create_post_view, name='create-post'),
    path('update-post/<int:pk>/', views.update_post_view, name='update-post'),
    path('delete-post/<int:pk>/', views.delete_post_view, name='delete-post'),
    path('update-message/<int:pk>/', views.update_message_view, name='edit-message'),
    path('delete-message/<int:pk>/', views.delete_message_view, name='delete-message'),
    path('post/<int:pk>/', views.post_view, name='post'),
    path('profile/<int:pk>/', views.profile_view, name='profile'),
    path('messages/<str:username>/', views.private_messages_view, name='private-messages'),
    path('messages/<str:username>/send/', views.send_private_message_view, name='send-private-message'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('upvote-post/<int:pk>/', views.upvote_post_view, name='upvote-post'),
    path('update-user/', views.update_user_view, name='update-user'),
    path('downvote-post/<int:pk>/', views.downvote_post_view, name='downvote-post'),
    path('categories/', views.category_page_view, name='categories'),
    path('activity-page/', views.activity_page_view, name='activity-page'),
]