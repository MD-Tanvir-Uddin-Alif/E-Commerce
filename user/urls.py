from django.urls import path
from .views import RegisterView, LoginView, LogoutView, VerifyEmailView, UserProfileView, UserProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='rejister'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
]