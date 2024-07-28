from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from authentification.models import CustomUser
from notifications.models import Notification
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

    if user in room.request_members.all():
        messages.error(request, 'Waiting approval from admin')
        return redirect('home')
    elif user in room.members.all():
        messages.error(request, "You are already a member!")
        return redirect('home')
    else:
        room.request_members.add(user)
        room.save()

        notification = Notification.objects.create(user=room.room_owner)
        notification.add_message(f"{user.username} wants to join room {room.room_name}.")
        notification.save()

        messages.success(request, "Your demand has been sent")
        return redirect('home')

@login_required
def accept_member(request, user_wants_join, room_name):
    room = get_object_or_404(Room, room_name=room_name)
    user_wants_join = get_object_or_404(CustomUser, username=user_wants_join)
    owner = request.user

    if room.room_owner != owner:
        messages.error(request, f"You are not a owner for {room.room_name}!")
        return redirect('home')

    if user_wants_join in room.members.all():
        messages.error(request, f"{user_wants_join} is already a member for {room.room_name}!")
        return redirect('home')

    if user_wants_join not in room.request_members.all():
        messages.error(request, f"{user_wants_join} has to join {room.room_name} first!")
        return redirect('home')

    notification = Notification.objects.create(user=user_wants_join)
    notification.add_message(f"You are now a member of {room.room_name}")
    notification.save()

    room.request_members.remove(user_wants_join)
    room.members.add(user_wants_join)
    room.save()

    return redirect(reverse('room', args=[room_name]))

@login_required
def reject_member(request, user_wants_join, room_name):
    room = get_object_or_404(Room, room_name=room_name)
    user_wants_join = get_object_or_404(CustomUser, username=user_wants_join)
    owner = request.user

    if room.room_owner != owner:
        messages.error(request, f"You are not a owner for {room.room_name}!")
        return redirect('home')

    if user_wants_join in room.members.all():
        messages.error(request, f"{user_wants_join} is already a member for {room.room_name}!")
        return redirect('home')

    if user_wants_join not in room.request_members.all():
        messages.error(request, f"{user_wants_join} has to join {room.room_name} first!")
        return redirect('home')

    notification = Notification.objects.create(user=user_wants_join)
    notification.add_message(f"Your demand to join {room.room_name} has been rejected")
    notification.save()

    room.request_members.remove(user_wants_join)
    room.save()

    return redirect(reverse('room', args=[room_name]))

@login_required
def room(request, room_name):
    room = get_object_or_404(Room, room_name=room_name)
    if request.user not in room.members.all():
        messages.error(request, "You are not a member!")
        return redirect('home')

    room_owner = request.user == room.room_owner
    members = room.members.all()
    for member in room.request_members.all():
        print(f"ici {member}")
    request_members = room.request_members.all() if room_owner else None
    return render(request,'room/room.html', {
        'room_name': room_name,
        'user_name': request.user.username,
        'room_owner': room_owner,
        'members': members,
        'request_members': request_members,
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

