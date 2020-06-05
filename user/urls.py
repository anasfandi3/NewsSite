from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.user_comments, name='user_comments'),
    path('posts/', views.user_posts, name='user_posts'),
    path('new_post/', views.user_new_post, name='user_new_post'),
    path('edit_post/<int:id>', views.user_edit_post, name='user_edit_post'),
    path('delete_post/<int:id>', views.user_delete_post, name='user_delete_post'),
    path('likes/', views.user_likes, name='user_likes'),
    path('delete_comment/<int:id>', views.delete_comment, name='delete_comment'),
    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),
]