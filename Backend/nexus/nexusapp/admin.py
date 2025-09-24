
from django.contrib import admin
from .models import UserBasicData

# Register only our custom models (User is already registered by Django)
admin.site.register(UserBasicData)