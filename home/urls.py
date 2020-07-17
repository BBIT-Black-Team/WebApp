from django.urls import path
from .views import login_view, faculty_register_view, home_view, logout_view

urlpatterns= [
    path('', home_view, name='home'),
    path('login', login_view, name='login'),
    path('register', faculty_register_view, name='register'),
    path('logout', logout_view, name='logout')
]