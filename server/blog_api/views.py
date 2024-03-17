from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import BlogSerializer, UpdateBlogSerializer
from .models import Blog
from rest_framework.response import Response
from rest_framework import status
import jwt, datetime

# Create your views here.

def get_user(token):
  # getting the user id from the token
  try:
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    return payload['id']
  except jwt.ExpiredSignatureError:
    return Response({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
  except jwt.InvalidTokenError:
    return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

class CreateBlogView(APIView):
  def post(self, request):
    token = request.COOKIES.get('jwt')

    # check if the user is logged in
    if not token:
      return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    # get the user id from the token
    user_id = get_user(token)

    # add the user id to the request data
    request.data['user_id'] = user_id
    serializer = BlogSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)

class GetAllBlogsView(APIView):
  def get(self, request):
    token = request.COOKIES.get('jwt')
    
    if not token:
      return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    user_id = get_user(token)

    # get all the blogs of the user
    try:
      blogs = Blog.objects.filter(user_id=user_id)
    except:
      return Response({'error': 'No blogs found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BlogSerializer(blogs, many=True)
    
    return Response(serializer.data)

class GetBlogView(APIView):
  def get(self, request, id):
    token = request.COOKIES.get('jwt')

    if not token:
      return Response({error: 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    user_id = get_user(token)

    # get the blog by id
    try:
      blog = Blog.objects.get(id=id)
    except:
      return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

    if blog.user_id != user_id:
      return Response({'error': 'You are not authorized to view this blog'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = BlogSerializer(blog)
    
    return Response(serializer.data)

  def put(self, request, id):
    token = request.COOKIES.get('jwt')
    
    if not token:
      return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    user_id = get_user(token)

    try:
      blog = Blog.objects.get(id=id)
    except:
      return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

    if blog.user_id != user_id:
      return Response({'error': 'You are not authorized to edit this blog'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = UpdateBlogSerializer(blog, data=request.data, partial=True) # set partial=True to update a data partially
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return Response(serializer.data)

  def delete(self, request, id):
    token = request.COOKIES.get('jwt')
    if not token:
      return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    user_id = get_user(token)

    try:
      blog = Blog.objects.get(id=id)
    except:
      return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

    if blog.user_id != user_id:
      return Response({'error': 'You are not authorized to delete this blog'}, status=status.HTTP_401_UNAUTHORIZED)

    blog.delete()
    return Response({'success': 'Blog deleted'}, status=status.HTTP_204_NO_CONTENT)