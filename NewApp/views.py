from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from rest_framework import permissions, status
from django.contrib.auth import get_user_model
from .utils import Utils
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings

# Create your views here.

User = get_user_model()
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
       
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hii '+user.username+' Thanks for registering with us, Kindly Verify Your Mail for Login \n' + absurl
        data = {'email_body': email_body, 'to_email':user.email, 'email_subject': 'Verify Your Mail'}


        Utils.send_email(data)

        return Response({"Message": "Thanks for Registration"})

class VerifyEmail(APIView):
    def get(self,request):
        token = request.GET.get('token')
        print("Hello")
        try:
            print("Hii")
            payload = jwt.decode(token, settings.SECRET_KEY)
            print(payload)
            user = User.objects.get(id=payload['user_id'])
            print(user)
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'message': 'Activation Successful'}, status=status.HTTP_200_OK)
        
        except jwt.ExpiredSignatureError as identifier:
            return Response({'message':'Activation Link Expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'message':'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

