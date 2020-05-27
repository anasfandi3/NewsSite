from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('addcomment/<int:post_id>', views.addcomment, name='addcomment'),
    path('like/', views.like, name='like_url')
    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),
]