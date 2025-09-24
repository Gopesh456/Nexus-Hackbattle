
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from .serializers import UserSerializer, FoodInputSerializer, FoodNutritionSerializer
from .models import FoodNutrition
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import json


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Please provide both username and password'},
                      status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            })
        else:
            return Response({'error': 'Invalid credentials'},
                          status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'},
                      status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User registered successfully',
            'user_id': user.id,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_food_nutrition(request):
    """
    Get nutrition information for a food item from USDA API and store it
    Expected input: {"food_name": "apple", "quantity": 150}
    """
    serializer = FoodInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    food_name = serializer.validated_data['food_name']
    quantity = serializer.validated_data['quantity']
    
    try:
        # Step 1: Search for the food item in USDA database
        search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
        search_params = {
            'api_key': settings.USDA_API_KEY,
            'query': food_name,
            'dataType': ['Foundation', 'SR Legacy'],
            'pageSize': 1
        }
        
        search_response = requests.get(search_url, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()
        
        if not search_data.get('foods'):
            return Response({
                'error': f'No nutrition data found for "{food_name}"'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get the first (most relevant) food item
        food_item = search_data['foods'][0]
        fdc_id = food_item['fdcId']
        
        # Step 2: Get detailed nutrition information
        detail_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
        detail_params = {'api_key': settings.USDA_API_KEY}
        
        detail_response = requests.get(detail_url, params=detail_params)
        detail_response.raise_for_status()
        nutrition_data = detail_response.json()
        
        # Step 3: Extract nutrient information
        nutrients = {}
        nutrient_mapping = {
            'Energy': 'calories',
            'Protein': 'protein',
            'Carbohydrate, by difference': 'carbohydrates',
            'Total lipid (fat)': 'fat',
            'Fiber, total dietary': 'fiber',
            'Sugars, total including NLEA': 'sugar'
        }
        
        for nutrient in nutrition_data.get('foodNutrients', []):
            nutrient_name = nutrient.get('nutrient', {}).get('name', '')
            nutrient_value = nutrient.get('amount', 0)
            
            for usda_name, our_name in nutrient_mapping.items():
                if usda_name in nutrient_name:
                    nutrients[our_name] = round(nutrient_value, 2)
                    break
        
        # Ensure all nutrients have values (default to 0 if missing)
        for nutrient in nutrient_mapping.values():
            if nutrient not in nutrients:
                nutrients[nutrient] = 0.0
        
        # Step 4: Calculate nutrition for the specified quantity
        multiplier = quantity / 100  # USDA data is per 100g
        total_nutrition = {
            'calories': round(nutrients['calories'] * multiplier, 2),
            'protein': round(nutrients['protein'] * multiplier, 2),
            'carbohydrates': round(nutrients['carbohydrates'] * multiplier, 2),
            'fat': round(nutrients['fat'] * multiplier, 2),
            'fiber': round(nutrients['fiber'] * multiplier, 2),
            'sugar': round(nutrients['sugar'] * multiplier, 2)
        }
        
        # Step 5: Store in database
        food_nutrition = FoodNutrition.objects.create(
            food_name=food_name,
            quantity=quantity,
            usda_food_id=str(fdc_id),
            calories_per_100g=nutrients['calories'],
            protein_per_100g=nutrients['protein'],
            carbs_per_100g=nutrients['carbohydrates'],
            fat_per_100g=nutrients['fat'],
            fiber_per_100g=nutrients['fiber'],
            sugar_per_100g=nutrients['sugar']
        )
        
        # Step 6: Return response
        response_data = {
            'food_name': food_name,
            'quantity': quantity,
            'unit': 'grams',
            'nutrition_per_100g': nutrients,
            'total_nutrition': total_nutrition,
            'usda_food_name': nutrition_data.get('description', food_name),
            'stored_id': food_nutrition.id
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except requests.RequestException as e:
        return Response({
            'error': 'Failed to fetch nutrition data from USDA API',
            'details': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    except Exception as e:
        return Response({
            'error': 'An unexpected error occurred',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_nutrition_history(request):
    """
    Get the history of stored nutrition data
    """
    try:
        nutrition_records = FoodNutrition.objects.all().order_by('-created_at')[:50]  # Latest 50 records
        serializer = FoodNutritionSerializer(nutrition_records, many=True)
        return Response({
            'count': nutrition_records.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Failed to retrieve nutrition history',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

