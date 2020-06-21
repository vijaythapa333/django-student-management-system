
from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.home, name="home"),
    path('', views.loginPage, name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
]
