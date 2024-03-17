from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt, datetime
from dotenv import load_dotenv
import os
from .serializers import UserSerializer
from .models import User

load_dotenv()

ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
REFRESH_TOKEN_SECRET = os.environ.get('REFRESH_TOKEN_SECRET')

def generate_access_and_refresh_tokens(user_id):
  access_token = jwt.encode({
    'id': user_id,
    'exp': datetime.datetime.utcnow()
     + datetime.timedelta(minutes=1)}, ACCESS_TOKEN_SECRET, algorithm='HS256')
  refresh_token = jwt.encode({'id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)}, REFRESH_TOKEN_SECRET, algorithm='HS256')

  return access_token, refresh_token

# Create your views here.
class RegisterView(APIView):
  def post(self, request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
  def post(self, request):
    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first()
    if user is None:
      return Response({'error': 'Invalid email/password'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(password):
      return Response({'error': 'Invalid email/password'}, status=status.HTTP_400_BAD_REQUEST)

    # generate access and refresh tokens for the user.
    access_token, refresh_token = generate_access_and_refresh_tokens(user.id)

    response = Response()

    # set the access and refresh tokens as httponly cookies
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)

    response.data = {
      'access_token': access_token,
      'refresh_token': refresh_token
    }

    return response

class UserView(APIView):
  def get(self, request):
    token = request.COOKIES.get('access_token')

    if not token:
      return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
      payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      return Response({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)

    return Response(serializer.data)
  
class LogoutView(APIView):
    def post(self, request):
      response = Response()
      response.delete_cookie('access_token')
      response.delete_cookie('refresh_token')
      response.data = {
        'message': 'success'
      }

      return response
    
class RefreshTokenView(APIView):
  def get(self, request):
    # get the refresh token from the request
    incoming_refresh_token = request.COOKIES.get('refresh_token')

    # if there is no refresh token, return an error
    if not incoming_refresh_token:
      return Response({'error': 'No refresh token'}, status=status.HTTP_400_BAD_REQUEST)

    response = Response()

    # decode the refresh token and check if it has expired or if the payload is invalid
    try:
      payload = jwt.decode(incoming_refresh_token, 'topsecret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      # if the refresh token has expired, generate a new refresh token and return it
      refresh_token = generate_access_and_refresh_tokens(payload['id'])[1]
      
      response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
      
      response.data = {
        'refresh_token': refresh_token
      }

    # get the user from the payload
    user = User.objects.filter(id=payload['id']).first()

    # if the user is not found, return an error
    if user is None:
      return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)

    # generate a new access token for the user
    access_token = generate_access_and_refresh_tokens(user.id)[0]

    # return the new access token
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    
    response.data = {
      'access_token': access_token
    }

    return response
  