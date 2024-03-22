from django.urls import path

from transaction import views

urlpatterns = [
    path("<int:bill_id>/add-transaction", views.add_transaction, name="add_transaction"),
    path("<int:transaction_id>/delete-transaction", views.delete_transaction, name="delete_transaction"),
]
