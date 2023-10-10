from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from .models import User
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data, context={'request': request})  # Pass the request in the context
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"Email or Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})


@api_view(['GET', "POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"status": "ok"})

@api_view(['GET', "POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_token(request):
    try:
        old_token = Token.objects.get(user=request.user)
        old_token.delete()
    except Token.DoesNotExist:
        pass

    new_token, created = Token.objects.get_or_create(user=request.user)

    return Response({"message": "Token changed", "new_token": new_token.key}, status=status.HTTP_200_OK)
