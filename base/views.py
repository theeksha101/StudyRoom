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
from .service import RoomService, UserService
room_service = RoomService()
user_service = UserService()


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
    # http://127.0.0.1:8000/?r=ja (this is what icontains will do)
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
    print(request)
    if request.method == 'POST':
        inc_msg = request.POST.get('inc_msg')
        user = request.user
        room_service.create_message(user, inc_msg, pk)
        return redirect(reverse('room', args=[pk]))
    context = {'room': room_service.get_room(pk), 'messages': room_service.get_room_msg(pk)}
    return render(request, 'base/room.html', context)


def create_room(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            room_info = request.POST
            room_service.create_room(room_info)
            return redirect('home')
        form = RoomForm(request.POST)  # Did not make changes here; this instance will just display the form
        context = {'form': form}
        return render(request, 'base/room_form.html', context)
    else:
        return redirect('login_user')


def update_room(request, pk):
    if request.method == 'POST':
        room_info = request.POST
        room_service.update_room(room_info, pk)
        return redirect('home')
        
    form = room_service.get_form(pk=pk)
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def delete_room(request, pk):
    if request.method == 'POST':
        room_service.delete_room(pk)
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})



def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # These lines of code gets username and password from http
        password = request.POST.get('password')
        try:
            user = user_service.get_username(username=username)
            user = authenticate(request, username=username, password=password)
            if user is None: 
                # messages.error(request, "Username or password do not match")
                raise Exception("Username or password do not match")
            
            login(request, user)  # request parameter is essential to keep the authentication status and session cookie
            return redirect('home')
        except Exception as e:
            messages.error(request, str(e))
    
    return render(request, 'base/login_user.html')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    context = {}
    return render(request, 'base/logout_user.html', context)


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
            user_service.create_user(username=username, password=password1,
                email=email, first_name=first_name, last_name = last_name)
        return redirect('login-user')
    
    return render(request, 'base/register_user.html')


@csrf_exempt
@login_required
def toggle_follow(request):
    if request.method == 'POST':
        user = request.user
        topic = request.POST.get('topic_name')  
        try:
            user_service.unfollow_topic(user=user, topic=topic)  
            message = 'Unfollowed {}'.format(topic)
        except UserFollowing.DoesNotExist:
            user_service.follow_topic(user=user, topic=topic)  # if it DoesNotExist then follow
            message = 'Followed {}'.format(topic)
        
        return JsonResponse({'message':message})
    else:
        return JsonResponse({'error': 'Invalid request method'})

