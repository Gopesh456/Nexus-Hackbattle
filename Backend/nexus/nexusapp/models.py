
from django.db import models

class User(models.Model):
	username = models.CharField(max_length=150, unique=True)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=128)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.username


class FoodNutrition(models.Model):
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
