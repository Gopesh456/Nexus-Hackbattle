from django.urls import path
from .views import register_user, login_user,store_user_basic_data, get_user_basic_data,store_user_health_profile, get_user_health_profile, store_blood_test_report, get_blood_test_report, store_metabolic_panel, get_metabolic_panel, store_liver_function_test, get_liver_function_test, store_medication_details, get_medication_details, get_food_nutrition, edit_nutrition_item, delete_nutrition_item, get_nutrition_history, nutrition_goals, daily_nutrition_summary, store_appointment, get_appointments, store_lab_report, get_lab_reports, get_lab_report_file
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
    path('nutrition/edit/', edit_nutrition_item, name='edit_nutrition_item'),
    path('nutrition/delete/', delete_nutrition_item, name='delete_nutrition_item'),
    path('nutrition/history/', get_nutrition_history, name='get_nutrition_history'),
    path('nutrition/goals/', nutrition_goals, name='nutrition_goals'),
    path('nutrition/summary/', daily_nutrition_summary, name='daily_nutrition_summary'),
    path('appointments/store/', store_appointment, name='store_appointment'),
    path('appointments/get/', get_appointments, name='get_appointments'),
    path('lab-reports/store/', store_lab_report, name='store_lab_report'),
    path('lab-reports/get/', get_lab_reports, name='get_lab_reports'),
    path('lab-reports/file/', get_lab_report_file, name='get_lab_report_file'),
]
