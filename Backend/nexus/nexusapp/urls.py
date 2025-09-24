from django.urls import path
from .views import (
    register_user, login_user, 
    store_user_basic_data, get_user_basic_data,
    store_user_health_profile, get_user_health_profile
)
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
]
