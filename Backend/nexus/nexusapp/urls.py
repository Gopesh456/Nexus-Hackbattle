from django.urls import path
from .views import register_user, login_user,store_user_basic_data, get_user_basic_data,store_user_health_profile, get_user_health_profile, store_blood_test_report, get_blood_test_report, store_metabolic_panel, get_metabolic_panel, store_liver_function_test, get_liver_function_test, get_food_nutrition, get_nutrition_history, nutrition_goals, daily_nutrition_summary
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('basic-info/store/', store_user_basic_data, name='store_user_basic_data'),
    path('basic-info/get/', get_user_basic_data, name='get_user_basic_data'),
    path('health-profile/store/', store_user_health_profile, name='store_user_health_profile'),
    path('health-profile/get/', get_user_health_profile, name='get_user_health_profile'),
    path('blood-test/store/', store_blood_test_report, name='store_blood_test_report'),
    path('blood-test/get/', get_blood_test_report, name='get_blood_test_report'),
    path('metabolic-panel/store/', store_metabolic_panel, name='store_metabolic_panel'),
    path('metabolic-panel/get/', get_metabolic_panel, name='get_metabolic_panel'),
    path('liver-function-test/store/', store_liver_function_test, name='store_liver_function_test'),
    path('liver-function-test/get/', get_liver_function_test, name='get_liver_function_test'),
    path('nutrition/', get_food_nutrition, name='get_food_nutrition'),
    path('nutrition/history/', get_nutrition_history, name='get_nutrition_history'),
    path('nutrition/goals/', nutrition_goals, name='nutrition_goals'),
    path('nutrition/summary/', daily_nutrition_summary, name='daily_nutrition_summary'),
]
