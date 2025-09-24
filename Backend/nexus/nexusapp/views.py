
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .models import User, UserBasicData
from .serializers import UserSerializer, UserBasicDataSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Please provide both username and password'},
                      status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Find user with matching username and password
        user = User.objects.get(username=username, password=password)
        
        # Create a custom JWT token with user ID
        from rest_framework_simplejwt.tokens import AccessToken
        token = AccessToken()
        token['user_id'] = user.id
        token['username'] = user.username
        
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'tokens': str(token)
        })
        
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'},
                      status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Create a custom JWT token with user ID
        from rest_framework_simplejwt.tokens import AccessToken
        token = AccessToken()
        token['user_id'] = user.id
        token['username'] = user.username
        
        return Response({
            'message': 'User registered successfully',
            'user': serializer.data,
            'tokens': str(token)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def store_user_basic_data(request):
    # Get token from request body
    token = request.data.get('token')
    
    if not token:
        return Response({
            'error': 'Token is required'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Validate JWT token
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(token)
        
        # Get user ID from token
        user_id = validated_token.get('user_id')
        if not user_id:
            return Response({
                'error': 'Invalid token - no user ID found'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get our custom user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({
            'error': 'Invalid token provided'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check if user already has basic data
    try:
        basic_data = UserBasicData.objects.get(user=user)
        serializer = UserBasicDataSerializer(basic_data, data=request.data)
    except UserBasicData.DoesNotExist:
        serializer = UserBasicDataSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(user=user)
        return Response({
            'message': 'User basic data stored successfully'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_user_basic_data(request):
    # Get token from request body
    token = request.data.get('token')
    
    if not token:
        return Response({
            'error': 'Token is required'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Validate JWT token
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(token)
        
        # Get user ID from token
        user_id = validated_token.get('user_id')
        if not user_id:
            return Response({
                'error': 'Invalid token - no user ID found'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get our custom user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({
            'error': 'Invalid token provided'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        basic_data = UserBasicData.objects.get(user=user)
        serializer = UserBasicDataSerializer(basic_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except UserBasicData.DoesNotExist:
        return Response({
            'error': 'No basic data found for this user'
        }, status=status.HTTP_404_NOT_FOUND)
