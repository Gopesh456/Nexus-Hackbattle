
from django.db import models
from django.contrib.auth.models import User as AuthUser

class User(models.Model):
	username = models.CharField(max_length=150, unique=True)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=128)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.username


class UserNutritionGoals(models.Model):
	"""Store user's daily nutrition goals"""
	user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='nutrition_goals')
	daily_calories_goal = models.FloatField(default=2000.0, help_text="Daily calorie goal")
	daily_protein_goal = models.FloatField(default=50.0, help_text="Daily protein goal in grams")
	daily_carbs_goal = models.FloatField(default=250.0, help_text="Daily carbohydrates goal in grams")
	daily_fat_goal = models.FloatField(default=65.0, help_text="Daily fat goal in grams")
	daily_fiber_goal = models.FloatField(default=25.0, help_text="Daily fiber goal in grams")
	daily_sugar_goal = models.FloatField(default=50.0, help_text="Daily sugar goal in grams")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.user.username}'s Nutrition Goals"


class FoodNutrition(models.Model):
	user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='food_entries', null=True, blank=True)  # Link to authenticated user
	food_name = models.CharField(max_length=255)
	quantity = models.FloatField()  # in grams
	usda_food_id = models.CharField(max_length=100, null=True, blank=True)
	
	# Macronutrients (per 100g)
	calories_per_100g = models.FloatField(null=True, blank=True)
	protein_per_100g = models.FloatField(null=True, blank=True)  # in grams
	carbs_per_100g = models.FloatField(null=True, blank=True)   # in grams
	fat_per_100g = models.FloatField(null=True, blank=True)     # in grams
	fiber_per_100g = models.FloatField(null=True, blank=True)   # in grams
	sugar_per_100g = models.FloatField(null=True, blank=True)   # in grams
	
	# Calculated values for the actual quantity
	total_calories = models.FloatField(null=True, blank=True)
	total_protein = models.FloatField(null=True, blank=True)
	total_carbs = models.FloatField(null=True, blank=True)
	total_fat = models.FloatField(null=True, blank=True)
	total_fiber = models.FloatField(null=True, blank=True)
	total_sugar = models.FloatField(null=True, blank=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"{self.food_name} - {self.quantity}g"
	
	def save(self, *args, **kwargs):
		# Calculate total values based on quantity
		if self.quantity and self.calories_per_100g:
			multiplier = self.quantity / 100
			self.total_calories = self.calories_per_100g * multiplier
			self.total_protein = (self.protein_per_100g or 0) * multiplier
			self.total_carbs = (self.carbs_per_100g or 0) * multiplier
			self.total_fat = (self.fat_per_100g or 0) * multiplier
			self.total_fiber = (self.fiber_per_100g or 0) * multiplier
			self.total_sugar = (self.sugar_per_100g or 0) * multiplier
		super().save(*args, **kwargs)
	
	@classmethod
	def get_daily_totals(cls, user, date=None):
		"""Calculate total nutrition for a user on a specific date"""
		from datetime import date as dt_date
		if date is None:
			date = dt_date.today()
		
		# Get all food entries for the user on the specified date
		entries = cls.objects.filter(
			user=user,
			created_at__date=date
		)
		
		totals = {
			'total_calories': sum(entry.total_calories or 0 for entry in entries),
			'total_protein': sum(entry.total_protein or 0 for entry in entries),
			'total_carbs': sum(entry.total_carbs or 0 for entry in entries),
			'total_fat': sum(entry.total_fat or 0 for entry in entries),
			'total_fiber': sum(entry.total_fiber or 0 for entry in entries),
			'total_sugar': sum(entry.total_sugar or 0 for entry in entries),
			'entries_count': entries.count()
		}
		
		return totals
