
from django.contrib import admin
from .models import UserBasicData, UserHealthProfile, BloodTestReport, MetabolicPanel, LiverFunctionTest, Appointment, LabReport

# Register only our custom models (User is already registered by Django)
admin.site.register(UserBasicData)
admin.site.register(UserHealthProfile)
admin.site.register(BloodTestReport)
admin.site.register(MetabolicPanel)
admin.site.register(LiverFunctionTest)

# Custom admin for Appointment model with better display
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor_name', 'doctor_specialization', 'appointment_date', 'appointment_type', 'location']
    list_filter = ['appointment_type', 'doctor_specialization', 'appointment_date']
    search_fields = ['doctor_name', 'user__username', 'location', 'reason']
    ordering = ['-appointment_date']
    date_hierarchy = 'appointment_date'


# Custom admin for LabReport model with better display
@admin.register(LabReport)
class LabReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'report_name', 'report_type', 'lab_name', 'doctor_name', 'report_date', 'file_size_display', 'created_at']
    list_filter = ['report_type', 'report_date', 'file_type', 'created_at']
    search_fields = ['report_name', 'user__username', 'lab_name', 'doctor_name', 'file_name']
    ordering = ['-report_date', '-created_at']
    date_hierarchy = 'report_date'
    readonly_fields = ['file_size', 'created_at', 'updated_at']
    
    def file_size_display(self, obj):
        return f"{obj.get_file_size_mb()} MB"
    file_size_display.short_description = 'File Size'