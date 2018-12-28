from django.urls import path
from .views import home, my_logout, HomePageView, MyView
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', home, name="home"),
    path('view/', MyView.as_view(), name="myView"),
    path('logout/', my_logout, name="logout"),
]
