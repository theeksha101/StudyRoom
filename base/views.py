from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {'id': 1, 'name':'Python'},
#     {'id': 2, 'name':'Designers'},
#     {'id': 3, 'name':'Frontend Developers'}
# ]



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
    topic = Topic.objects.all()
    room_count = rooms.count()
    all_users = User.objects.values()
    # all_user = User.objects.get(username='deeksha')
    context = {'rooms': rooms, 'topics': topic, 'room_count': room_count,
               'all_users': all_users}
    # print(all_user)
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
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


def is_following(request, id_):
    is_follow = Topic.objects.get(id=id_)
    if is_follow.follow == False:
        is_follow.follow = True
        is_follow.save()
    else:
        is_follow.follow = False
        is_follow.save()
    return redirect('home')


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
