from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from room.forms import CreateRoomForm
from room.models import Room

class homeView(TemplateView):
    template_name = "home.html"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        rooms = Room.objects.all().values('room_name', 'id')
        form_create_room = CreateRoomForm()
        rooms_with_membership = [
            {**room, 'user_is_member': request.user in Room.objects.get(id=room['id']).members.all()}
            for room in rooms
        ]
        return render(request, self.template_name, {
            'form_create_room': form_create_room,
            'rooms': rooms_with_membership,
            'user': request.user,
        })
