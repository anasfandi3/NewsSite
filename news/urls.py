from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('addcomment/<int:post_id>', views.addcomment, name='addcomment'),
    path('like/<int:post_id>', views.like, name='like')
    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),
]