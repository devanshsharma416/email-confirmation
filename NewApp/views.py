import imp
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from rest_framework import permissions
from rest_framework.simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from utils import Utils
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
# Create your views here.

User = get_user_model
class RegisterUser(APIView):
    
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
       
        current_site = get_current_site(request) 
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+token
        email_body = 'Hii'+user.first_name+'Thanks for registering with us, verify your mail \n' + absurl
        data = {'email_body': email_body, 'email_subject': 'Verify Your Mail'}


        Utils.send_email(data)


        return HttpResponse('<h1>Hello</h2>')


class VerifyEmail(APIView):
    def get():
        pass
# def login(request):
#     return HttpResponse('<h1>Hii</h2>')