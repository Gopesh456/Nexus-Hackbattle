
from django.db import models

class User(models.Model):
	username = models.CharField(max_length=150, unique=True)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=128)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.username

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
