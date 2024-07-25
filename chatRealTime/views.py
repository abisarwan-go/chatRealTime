from django.shortcuts import render
from django.views.generic import TemplateView

from room.forms import CreateRoomForm
from room.models import Room

class homeView(TemplateView):
    template_name = "home.html"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        rooms = Room.objects.all()
        form_create_room = CreateRoomForm()
        return render(request, self.template_name, {
            'form_create_room': form_create_room,
            'rooms': rooms,
            'user': request.user
        })
