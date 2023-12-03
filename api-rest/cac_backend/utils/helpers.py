import jwt
from datetime import datetime, timedelta
from cac_backend.settings import SECRET_JWT
from app.models import User

from rest_framework.response import Response

def create_token(payload):
  payload = { **payload, 'exp': datetime.utcnow() + timedelta(minutes=30)}
  return jwt.encode(payload, SECRET_JWT, algorithm='HS256')

def decode_token(token):
  return jwt.decode(token, SECRET_JWT, algorithms=['HS256'])

def check_login(request):
  authorization = request.headers.get('Authorization')

  if authorization is None:
    return 'Token not found'

  try:
    userToken = decode_token(authorization)
  except jwt.exceptions.ExpiredSignatureError:
    return  'Token expired'

  if User.objects.get(pk=userToken['id']).is_admin is False or User.objects.get(pk=userToken['id']).is_active is False or User.objects.get(pk=userToken['id']) is None: 
    return 'Unauthorized'

  return userToken