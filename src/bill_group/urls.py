from django.urls import path

from bill_group import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create_bill_group"),
    path("<int:group_id>/update", views.update, name="update_bill_group"),
    path("group/<str:hash_ids>", views.group_index, name="group_index"),
]
