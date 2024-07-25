from django import forms
from room.models import Room


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_name',)

