"""
URL configuration for agri_p project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from.import views


urlpatterns = [
    path('',views.index,name="home"),
    path('home_cons',views.home_cons,name="home_cons"),
    path('home_farmer',views.home_farmer,name="home_farmer"),
    path('signup_login',views.signup_login,name="signup_login"),
    path('shop',views.shop,name="shop"),
    path('login',views.login,name="login"),
    path('signup',views.signup,name="signup"),
    path('logout',views.logout,name="logout"),
]