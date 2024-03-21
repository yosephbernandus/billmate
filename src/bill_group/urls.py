from django.urls import path

from bill_group import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create_bill_group"),
    path("<int:group_id>/update", views.update, name="update_bill_group"),
    path("group/<int:group_id>/bills", views.bill_index, name="group_bill_index"),
    path("group/<str:hash_ids>", views.group_index, name="group_index"),

    # Bill
    path("group/<int:group_id>/add-bill", views.add_bill, name="group_add_bill"),
    path("group/<int:group_id>/update-bill/<int:bill_id>", views.update_bill, name="group_update_bill"),
    path("group/<int:group_id>/detail-bill/<int:bill_id>", views.detail_bill, name="group_detail_bill"),
]
