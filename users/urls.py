from django.urls import path
from .views import *

urlpatterns = [
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path('login/', LoginUserView.as_view(), name='login'),
    # path('register/', RegisterUserView.as_view(), name='register'),
    # path('profile/', ProfileView.as_view(), name='profile'),
]