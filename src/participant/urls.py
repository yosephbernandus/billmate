from django.urls import path

from participant import views

urlpatterns = [
    path("group/<int:group_id>/add", views.add_participant, name="add_participant"),
    path("group/<int:group_id>/<int:participant_id>/delete", views.delete_participant, name="delete_participant"),
]
