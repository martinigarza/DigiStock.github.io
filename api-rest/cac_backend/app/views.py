from django.http import HttpResponse
from utils.helpers import check_login, create_token, decode_token

from app.models import Product, User
from app.serializers import ProductSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.hashers import make_password, check_password

# Import secret jwt from settings
from cac_backend.settings import SECRET_JWT

# Create your views here.
def index(request):
  return HttpResponse('<h1> API REST - DigiStock </h1>')

# Products
@api_view(['GET', 'POST']) 
def get_products(request):
  if request.method == 'GET':
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
  
  elif request.method == 'POST':
    authorization = check_login(request)

    if type(authorization) is str:
      return Response(status=401, data={'error': authorization})

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400) 

  
@api_view(['GET', 'PUT', 'DELETE'])
def get_product(request, pk):
  try:
    product = Product.objects.get(pk=pk)
  except Product.DoesNotExist:
    return Response(status=404, data={'error': 'Product not found'})

  if request.method == 'GET':
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=200)

  elif request.method == 'PUT':
    authorization = check_login(request)

    if type(authorization) is str:
      return Response(status=401, data={'error': authorization})

    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

  elif request.method == 'DELETE':
    authorization = check_login(request)

    if type(authorization) is str:
      return Response(status=401, data={'error': authorization})

    product.delete()
    return Response(status=204, data={'message': 'Product deleted'})

# Users
@api_view(['GET'])
def get_users(request):
  authorization = check_login(request)

  if type(authorization) is str:
    return Response(status=401, data={'error': authorization})

  users = User.objects.all()
  serializer = UserSerializer(users, many=True)
  return Response(serializer.data)
  

@api_view(['GET', 'PUT', 'DELETE'])
def get_user(request, pk):
  authorization = check_login(request)

  if type(authorization) is str:
    return Response(status=401, data={'error': authorization})

  try:
    user = User.objects.get(pk=pk)
  except User.DoesNotExist:
    return Response(status=404, data={'error': 'User not found'})

  if request.method == 'GET':
    serializer = UserSerializer(user)
    return Response(serializer.data, status=200)

  elif request.method == 'PUT':
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

  elif request.method == 'DELETE':
    user.delete()
    return Response(status=204, data={'message': 'User deleted'})

# Login
@api_view(['POST'])
def login(request):
  username = request.data.get('username')
  password = request.data.get('password')

  try:
    user = User.objects.get(username=username)
  except User.DoesNotExist:
    return Response(status=404, data={'error': 'User not found'})
  
  if check_password(password, user.password):
    token = create_token({'username': username, 'id': user.id})
    return Response(status=200, data={'message': 'Login successful', 'token': token})
  
  return Response(status=401, data={'error': 'Unauthorized'})

# Register
@api_view(['POST'])
def register(request):
  user = request.data
  user['password'] = make_password(user['password'])

  serializer = UserSerializer(data=user)

  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=201)
  return Response(serializer.errors, status=400)