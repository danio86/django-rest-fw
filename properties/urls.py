from django.urls import path
from properties import views

urlpatterns = [
    path('properties/', views.PropertyList.as_view()),
    path('properties/<int:pk>/', views.PropertyDetail.as_view())
]
