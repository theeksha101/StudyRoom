from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from .models import Room, Topic, UserFollowing, Message
from .forms import RoomForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


def home(request):
    if request.GET.get('r') != None:
        r = request.GET.get('r')
    else:
        r = ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=r) |
        Q(name__icontains=r) |
        Q(description__icontains=r) 
        # Q(host__icontains=r)
        ) 
    # http://127.0.0.1:8000/?r=ja (this is what icontains wil do)
    topics = Topic.objects.all()
    room_count = rooms.count()
    all_users = User.objects.values()
    logged_in_user = str(request.user)
    topic_following = UserFollowing.objects.filter(user__username__contains=logged_in_user)
    list_topic_following = [str(topic_following[i].topic) for i in range(len(topic_following))]

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
               'all_users': all_users, 'list_topic_following': list_topic_following}

    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    # msg = Message.objects.all()
    messages = Message.objects.filter(room=pk)
    if request.method == 'POST':
        inc_msg = request.POST.get('inc_msg')
        msg = Message.objects.create(user=request.user, room=room, body=inc_msg)
        msg.save()
        return redirect(reverse('room', args=[pk]))
    context = {'room': room, 'messages': messages}
    return render(request, 'base/room.html', context)


def create_room(request):
    if request.user.is_authenticated:
        form = RoomForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('home')
        context = {'form': form}
        print(form)
        return render(request, 'base/room_form.html', context)
    else:
        return redirect('login_register')

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


def login_user(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password does not match')

    return render(request, 'base/login_user.html')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    context = {}
    return render(request, 'base/logout_user.html', context)


@csrf_exempt
@login_required
def toggle_follow(request):
    if request.method == 'POST':
        user = request.user
        topic_name = request.POST.get('topic_name')
        topic = Topic.objects.get(name=topic_name)

        try:
            follow_entry = UserFollowing.objects.get(user=user, topic=topic)
            print(follow_entry)  # Here is the problem
            follow_entry.delete()
            message = 'Unfollowed {}'.format(topic_name)
        except UserFollowing.DoesNotExist:
            UserFollowing.objects.create(user=user, topic=topic)
            message = 'Followed {}'.format(topic_name)
        
        return JsonResponse({'message':message})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def register_user(request):
    if request.method == 'POST':

        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'passwords do not match')
        else:
            user = User.objects.create_user(username=username,
                        password=password1, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        return redirect('login-user')
    
    return render(request, 'base/register_user.html')
