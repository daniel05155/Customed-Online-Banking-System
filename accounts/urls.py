from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ="home"),
    path('login/', views.login_user, name ='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('change-password/', views.change_password, name='change_password'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('set-session-timeout/', views.set_session_timeout, name='set_session_timeout'),
    path('reset-timer/', views.reset_timer, name='reset_timer'),
    
]

