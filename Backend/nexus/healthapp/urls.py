from django.urls import path
from . import views, lab_views

app_name = 'healthapp'

urlpatterns = [
    # API endpoints for data-or-input pattern
    path('api/profile/', views.user_profile_data_or_input, name='profile_data_or_input'),
    path('api/medicines/', views.medicine_data_or_input, name='medicine_data_or_input'),
    path('api/appointments/', views.appointment_data_or_input, name='appointment_data_or_input'),
    path('api/lab-results/', views.lab_results_data, name='lab_results_data'),
    path('api/check-data/', views.check_data_availability, name='check_data_availability'),
    
    # Lab report image processing endpoints
    path('api/lab-image-upload/', lab_views.upload_lab_report_image, name='upload_lab_report'),
    path('api/lab-text-analyze/', lab_views.analyze_lab_text, name='analyze_lab_text'),
    path('api/lab-batch-process/', lab_views.batch_process_lab_reports, name='batch_process_labs'),
    path('api/lab-status/', lab_views.get_lab_report_status, name='lab_report_status'),
]