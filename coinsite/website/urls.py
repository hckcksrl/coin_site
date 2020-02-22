from django.urls import path
from . import views

urlpatterns = [
    path('coin/<str:site>/', views.CoinOne.as_view()),
    path('search', views.Search.as_view())
]
