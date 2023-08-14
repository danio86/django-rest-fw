from django.urls import path
from posts import views

urlpatterns = [
    path('properties/', views.PostList.as_view()),
    path('properties/<int:pk>/', views.PostDetail.as_view())
]
