
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
from django.conf import settings
from .serializers import UserSerializer, FoodInputSerializer, FoodNutritionSerializer, UserNutritionGoalsSerializer, DailyNutritionSummarySerializer
from .models import FoodNutrition, UserNutritionGoals
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date, datetime
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Changed to require authentication
def get_food_nutrition(request):
    """
    Get nutrition information for a food item from USDA API and store it for the authenticated user
    Expected input: {"food_name": "apple", "quantity": 150}
    Headers: Authorization: Bearer <jwt_token>
    """
    serializer = FoodInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    food_name = serializer.validated_data['food_name']
    quantity = serializer.validated_data['quantity']
    user = request.user  # Get the authenticated user from JWT token
    
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
        
        # Step 5: Store in database for the authenticated user
        food_nutrition = FoodNutrition.objects.create(
            user=user,  # Associate with the authenticated user
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Changed to require authentication
def get_nutrition_history(request):
    """
    Get the history of stored nutrition data for the authenticated user
    Headers: Authorization: Bearer <jwt_token>
    Body: {} (empty JSON object for POST request)
    """
    try:
        user = request.user  # Get the authenticated user from JWT token
        nutrition_records = FoodNutrition.objects.filter(user=user).order_by('-created_at')[:50]  # Latest 50 records for this user
        serializer = FoodNutritionSerializer(nutrition_records, many=True)
        return Response({
            'user': user.username,
            'count': nutrition_records.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Failed to retrieve nutrition history',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nutrition_goals(request):
    """
    POST: Get or set/update user's nutrition goals
    Headers: Authorization: Bearer <jwt_token>
    Body: 
    - To get goals: {"action": "get"}
    - To set/update goals: {"action": "set", "daily_calories_goal": 2500, "daily_protein_goal": 100, ...}
    """
    user = request.user
    action = request.data.get('action', 'get')
    
    if action == 'get':
        try:
            goals, created = UserNutritionGoals.objects.get_or_create(
                user=user,
                defaults={
                    'daily_calories_goal': 2000.0,
                    'daily_protein_goal': 50.0,
                    'daily_carbs_goal': 250.0,
                    'daily_fat_goal': 65.0,
                    'daily_fiber_goal': 25.0,
                    'daily_sugar_goal': 50.0
                }
            )
            serializer = UserNutritionGoalsSerializer(goals)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Failed to retrieve nutrition goals',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif action == 'set':
        try:
            goals, created = UserNutritionGoals.objects.get_or_create(user=user)
            serializer = UserNutritionGoalsSerializer(goals, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                action_result = "created" if created else "updated"
                return Response({
                    'message': f'Nutrition goals {action_result} successfully',
                    'goals': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'error': 'Failed to update nutrition goals',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return Response({
            'error': 'Invalid action. Use "get" or "set"'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def daily_nutrition_summary(request):
    """
    Get daily nutrition summary with goals comparison
    Headers: Authorization: Bearer <jwt_token>
    Body: {"date": "YYYY-MM-DD"} (optional, defaults to today if not provided)
    """
    user = request.user
    
    try:
        # Parse date parameter or use today
        date_param = request.data.get('date')
        if date_param:
            try:
                target_date = datetime.strptime(date_param, '%Y-%m-%d').date()
            except ValueError:
                return Response({
                    'error': 'Invalid date format. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            target_date = date.today()
        
        # Get daily totals
        daily_totals = FoodNutrition.get_daily_totals(user, target_date)
        
        # Get user's goals
        goals, created = UserNutritionGoals.objects.get_or_create(
            user=user,
            defaults={
                'daily_calories_goal': 2000.0,
                'daily_protein_goal': 50.0,
                'daily_carbs_goal': 250.0,
                'daily_fat_goal': 65.0,
                'daily_fiber_goal': 25.0,
                'daily_sugar_goal': 50.0
            }
        )
        
        # Calculate progress percentages
        consumed = {
            'calories': round(daily_totals['total_calories'], 2),
            'protein': round(daily_totals['total_protein'], 2),
            'carbohydrates': round(daily_totals['total_carbs'], 2),
            'fat': round(daily_totals['total_fat'], 2),
            'fiber': round(daily_totals['total_fiber'], 2),
            'sugar': round(daily_totals['total_sugar'], 2)
        }
        
        goals_dict = {
            'calories': goals.daily_calories_goal,
            'protein': goals.daily_protein_goal,
            'carbohydrates': goals.daily_carbs_goal,
            'fat': goals.daily_fat_goal,
            'fiber': goals.daily_fiber_goal,
            'sugar': goals.daily_sugar_goal
        }
        
        progress = {}
        for nutrient in consumed.keys():
            goal_value = goals_dict[nutrient]
            consumed_value = consumed[nutrient]
            if goal_value > 0:
                progress[f"{nutrient}_percentage"] = round((consumed_value / goal_value) * 100, 1)
                progress[f"{nutrient}_remaining"] = round(max(0, goal_value - consumed_value), 2)
            else:
                progress[f"{nutrient}_percentage"] = 0
                progress[f"{nutrient}_remaining"] = 0
        
        summary_data = {
            'date': target_date,
            'consumed': consumed,
            'goals': goals_dict,
            'progress': progress,
            'entries_count': daily_totals['entries_count']
        }
        
        return Response({
            'user': user.username,
            'summary': summary_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Failed to generate daily nutrition summary',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

