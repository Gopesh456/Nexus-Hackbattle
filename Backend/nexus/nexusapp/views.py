
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserBasicData, UserHealthProfile
from .serializers import UserSerializer, UserBasicDataSerializer, UserHealthProfileSerializer
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
    
    # Use Django's built-in authenticate function
    user = authenticate(username=username, password=password)
    
    if user:
        # Create JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'tokens': str(refresh.access_token)
        })
    else:
        return Response({'error': 'Invalid credentials'},
                      status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Create JWT token using Django's built-in User
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'tokens': str(refresh.access_token)
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
        
        # Get user from token using Django's built-in method
        user = jwt_auth.get_user(validated_token)
        
        if not user:
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
        
        # Get user from token using Django's built-in method
        user = jwt_auth.get_user(validated_token)
        
        if not user:
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

@api_view(['POST'])
@permission_classes([AllowAny])
def store_user_health_profile(request):
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
        
        # Get user from token using Django's built-in method
        user = jwt_auth.get_user(validated_token)
        
        if not user:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({
            'error': 'Invalid token provided'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Handle emergency_contact nested data
    request_data = request.data.copy()
    emergency_contact = request_data.pop('emergency_contact', None)
    if emergency_contact:
        request_data['emergency_contact_name'] = emergency_contact.get('name', '')
        request_data['emergency_contact_relationship'] = emergency_contact.get('relationship', '')
        request_data['emergency_contact_phone'] = emergency_contact.get('phone', '')
    
    # Check if user already has health profile
    try:
        health_profile = UserHealthProfile.objects.get(user=user)
        serializer = UserHealthProfileSerializer(health_profile, data=request_data, partial=True)
    except UserHealthProfile.DoesNotExist:
        serializer = UserHealthProfileSerializer(data=request_data)
    
    if serializer.is_valid():
        serializer.save(user=user)
        return Response({
            'message': 'User health profile stored successfully'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_user_health_profile(request):
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
        
        # Get user from token using Django's built-in method
        user = jwt_auth.get_user(validated_token)
        
        if not user:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({
            'error': 'Invalid token provided'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        health_profile = UserHealthProfile.objects.get(user=user)
        serializer = UserHealthProfileSerializer(health_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except UserHealthProfile.DoesNotExist:
        return Response({
            'error': 'No health profile found for this user'
        }, status=status.HTTP_404_NOT_FOUND)
