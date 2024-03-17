from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import BlogSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Blog
import jwt, datetime

# Create your views here.

def get_user(token):
  try:
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    return payload['id']
  except jwt.ExpiredSignatureError:
    return Response({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
  except jwt.InvalidTokenError:
    return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

class GetAllBlogsView(APIView):
  def get(self, request):
    token = request.COOKIES.get('jwt')
    if not token:
      return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    user_id = get_user(token)

    try:
      blogs = Blog.objects.filter(user_id=user_id)
    except:
      return Response({'error': 'No blogs found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)

class CreateBlogView(APIView):
  def post(self, request):
    token = request.COOKIES.get('jwt')
    if not token:
      return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    user_id = get_user(token)

    blog = request.data
    blog['user_id'] = user_id
    serializer = BlogSerializer(data=blog)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetBlogView(APIView):
  def get(self, request, id):
    token = request.COOKIES.get('jwt')
    if not token:
      return Response({error: 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    user_id = get_user(token)

    try:
      blog = Blog.objects.get(id=id)
    except:
      return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

    if blog.user_id != user_id:
      return Response({'error': 'You are not authorized to view this blog'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = BlogSerializer(blog)
    return Response(serializer.data)

