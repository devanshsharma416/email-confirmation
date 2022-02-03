from atexit import register
from django.urls import path
from .views import RegisterUser, VerifyEmail

urlpatterns = [
    path('', RegisterUser.as_view(), name='register'),
    path('email-verify', VerifyEmail.as_view(), name='email-verify')
]
