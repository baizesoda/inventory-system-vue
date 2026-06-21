from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.MeView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('users/', views.UserListView.as_view()),
]
