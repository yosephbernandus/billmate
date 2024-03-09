from django.urls import path

from bill_group import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create_bill_group"),
]
