from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.post_treasure, name='post'),
    path('get/<uuid:pk>/', views.get_treasure, name='get_treasure'),
    path('token/<uuid:pk>/', views.get_token, name='get_token'),
    path('assign_token/', views.assign_token, name='assign_token'),
    path('protect_token/', views.protect_token, name='protect_token'),
    path('get_new/', views.get_new_treasure, name='get_new_treasure'),
    path('signup/', views.register_user, name='registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('my_tokens/', views.my_tokens, name='my_tokens'),
    path('my_treasures/', views.my_treasures, name='my_treasures'),
    path('assign_treasure/', views.assign_treasure, name='assign_treasure'),
]
