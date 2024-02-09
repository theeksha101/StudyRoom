from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_user, name='login-user'),
    path('logout/', views.logout_user, name='logout-user'),
    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<str:pk>', views.update_room, name='update-room'),
    path('delete-room/<str:pk>', views.delete_room, name='delete-room'),
    # path('is-following/<str:id_>', views.is_following, name='is-following'),
    path('register/', views.register_user, name='register-user'),
    path('toggle_follow/', views.toggle_follow, name='toggle_follow'),
]