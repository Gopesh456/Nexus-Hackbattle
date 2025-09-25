
from django.contrib import admin
from .models import UserBasicData, UserHealthProfile, BloodTestReport, MetabolicPanel

# Register only our custom models (User is already registered by Django)
admin.site.register(UserBasicData)
admin.site.register(UserHealthProfile)
admin.site.register(BloodTestReport)
admin.site.register(MetabolicPanel)