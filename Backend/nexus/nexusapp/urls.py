from django.urls import path
from .views import register_user, login_user, get_food_nutrition, get_nutrition_history
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('nutrition/', get_food_nutrition, name='get_food_nutrition'),
    path('nutrition/history/', get_nutrition_history, name='get_nutrition_history'),
]
