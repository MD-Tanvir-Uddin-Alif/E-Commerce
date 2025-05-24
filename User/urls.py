from django.urls import path
from .views import UserModelView


urlpatterns = [
    path('registration/', UserModelView.as_view(),name='register'),
]
