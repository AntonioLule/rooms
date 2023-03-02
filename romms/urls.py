
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.views import (logout_then_login, LoginView)

#Views
from apps.rent.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login, Logout
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('registrar/', RegisterView.as_view(), name='register'),

    # Home - Inicio
    path('home/', home, name='home'),
    path('inicio/', Dashboard.as_view(), name='dash'),
    path('delete-room/<int:pk>/', delete_room, name='delete_room'),
    path('create-reserve/<int:pk>/<int:pk_customer>/', create_reserve, name='create_reserve'),
    path('cansele-reserve/<int:pk>/<int:pk_customer>/', cancel_reserve, name='cancel_reserve'),
    
    
]
