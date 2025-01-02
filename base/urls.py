from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('login/', views.login_user, name='login-user'),
    path('logout/', views.logout_user, name='logout-user'),
    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<str:pk>', views.update_room, name='update-room'),
    path('delete-room/<str:pk>', views.delete_room, name='delete-room'),
    path('register/', views.register_user, name='register-user'),
    path('toggle_follow/', views.toggle_follow, name='toggle_follow'),
    path('join_room/', views.join_room, name='join_room'),
    path('profile/<int:user_id>/<str:username>', views.user_profile, name='user_profile'),
    path('edit-profile/<int:user_id>/<str:username>', views.edit_profile, name='edit_profile'),
    path('follow_user/', views.follow_unfollow, name='follow_user'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)