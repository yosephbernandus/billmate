from django.urls import path

from home import views

urlpatterns = [
    path("", views.index, name="home"),
    path("logout", views.logout_view, name="logout"),
]
