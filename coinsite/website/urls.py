from django.urls import path
from . import views

urlpatterns = [
    path('coin/<str:site>/', views.GetCoin.as_view()),
    path('search', views.Search.as_view())
]
