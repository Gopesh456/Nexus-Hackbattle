
from django.db import models
from django.contrib.auth.models import User

class UserBasicData(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basic_data')
	full_name = models.CharField(max_length=255)
	date_of_birth = models.DateField()
	gender = models.CharField(max_length=50)
	location = models.CharField(max_length=255)
	email = models.EmailField()
	phone = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.full_name} - {self.user.username}"

class UserHealthProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_profile')
	height_cm = models.IntegerField()
	weight_kg = models.IntegerField()
	chronic_conditions = models.JSONField(default=list, blank=True)
	allergies = models.JSONField(default=list, blank=True)
	current_medications = models.JSONField(default=list, blank=True)
	blood_group = models.CharField(max_length=10)
	emergency_contact_name = models.CharField(max_length=255)
	emergency_contact_relationship = models.CharField(max_length=100)
	emergency_contact_phone = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Health Profile - {self.user.username}"
