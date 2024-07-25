from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from authentification.models import CustomUser
from room.forms import CreateRoomForm
from django.contrib import messages

from room.models import Room


@login_required
# Create your views here.
def create_room(request):
    if request.method == 'POST':
        form_create_room = CreateRoomForm(request.POST)
        if form_create_room.is_valid():
            room = form_create_room.save(commit=False)
            room.room_owner = request.user
            room.save()
            return redirect('home')
        else:
            errors = form_create_room.errors
            messages.error(request, errors)
            return redirect('home')
    else:
        return redirect('home')


@login_required
def join_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    user = request.user

    if user not in room.request_members.all():
        room.request_members.add(user)
        room.save()
    elif user in room.members.all():
        messages.error(request, "You are already a member!")
    else:
        messages.error(request, 'Waiting approval from admin')
    return redirect('home')


@login_required
def accept_room(request, user, room_id):
    room = get_object_or_404(Room, pk=room_id)
    owner = request.user

    if room.room_owner != owner:
        messages.error(request, f"You are not a owner for {room.room_name}!")
        return redirect('home')

    if user in room.members.all():
        messages.error(request, f"You are already a member for {room.room_name}!")
        return redirect('home')

    if user not in room.request_members.all():
        messages.error(request, f"You have to join {room.room_name} first!")
        return redirect('home')

    room.members.add(user)


def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    is_owner = request.user.is_authenticated and request.user.username == user.username

    if is_owner:
        rooms = user.owned_rooms.all()
    else:
        rooms = user.owned_rooms.only('room_name', 'room_owner', 'members')

    return render(request,'room/profile.html', {
                                                'rooms': rooms,
                                                'is_owner': is_owner
                                                })
@login_required
def room(request, room_name):
    room = get_object_or_404(Room, room_name=room_name)
    if request.user not in room.members.all():
        messages.error(request, "You are not a member!")
        return redirect('home')
    return render(request,'room/room.html', {
        'room_name': room_name,
    })


@login_required
def delete_room(request, room_name):
    room = get_object_or_404(Room, room_name=room_name)

    if request.user != room.room_owner:
        messages.error(request, "You are not a owner!")
        return redirect('home')

    room.delete()
    messages.success(request, f"Room {room_name} deleted!")
    return redirect('home')