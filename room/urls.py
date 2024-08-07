from django.urls import path
from . import views

urlpatterns = [
    path("create_room/", views.create_room, name="create_room"),

    path("join_room/<int:room_id>/", views.join_room, name="join_room"),

    path("<str:room_name>/", views.room , name="room"),

    path("delete_room/<str:room_name>/", views.delete_room, name="delete_room"),

    path("<str:room_name>/accept_member/<str:user_wants_join>/", views.accept_member , name="accept_member"),

    path("<str:room_name>/reject_member/<str:user_wants_join>/", views.reject_member , name="reject_member"),

]