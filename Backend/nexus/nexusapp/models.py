
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
	daily_calorie_goal = models.FloatField(default=2000.0, help_text="Daily calorie goal")
	daily_protein_goal = models.FloatField(default=50.0, help_text="Daily protein goal in grams")
	emergency_contact_name = models.CharField(max_length=255)
	emergency_contact_relationship = models.CharField(max_length=100)
	emergency_contact_phone = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Health Profile - {self.user.username}"


class BloodTestReport(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blood_test_report')
	
	# Complete Blood Count (CBC) parameters
	hemoglobin = models.CharField(max_length=50, blank=True, help_text="Hemoglobin level (e.g., '13.5 g/dL')")
	hematocrit = models.CharField(max_length=50, blank=True, help_text="Hematocrit percentage (e.g., '40%')")
	wbc_count = models.CharField(max_length=50, blank=True, help_text="White Blood Cell count (e.g., '7.2 x10^3/µL')")
	rbc_count = models.CharField(max_length=50, blank=True, help_text="Red Blood Cell count (e.g., '4.7 x10^6/µL')")
	platelet_count = models.CharField(max_length=50, blank=True, help_text="Platelet count (e.g., '250 x10^3/µL')")
	
	# Red Blood Cell Indices
	mcv = models.CharField(max_length=50, blank=True, help_text="Mean Corpuscular Volume (e.g., '90 fL')")
	mch = models.CharField(max_length=50, blank=True, help_text="Mean Corpuscular Hemoglobin (e.g., '30 pg')")
	mchc = models.CharField(max_length=50, blank=True, help_text="Mean Corpuscular Hemoglobin Concentration (e.g., '33 g/dL')")
	
	# Differential Count
	neutrophils = models.CharField(max_length=50, blank=True, help_text="Neutrophils percentage (e.g., '60%')")
	lymphocytes = models.CharField(max_length=50, blank=True, help_text="Lymphocytes percentage (e.g., '30%')")
	monocytes = models.CharField(max_length=50, blank=True, help_text="Monocytes percentage (e.g., '6%')")
	eosinophils = models.CharField(max_length=50, blank=True, help_text="Eosinophils percentage (e.g., '3%')")
	basophils = models.CharField(max_length=50, blank=True, help_text="Basophils percentage (e.g., '1%')")
	
	# Test metadata
	test_date = models.DateField(blank=True, null=True, help_text="Date when the blood test was conducted")
	lab_name = models.CharField(max_length=255, blank=True, help_text="Name of the laboratory")
	doctor_name = models.CharField(max_length=255, blank=True, help_text="Name of the ordering physician")
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Blood Test Report - {self.user.username}"


class MetabolicPanel(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='metabolic_panel')
	
	# Basic Metabolic Panel parameters
	glucose = models.CharField(max_length=50, blank=True, help_text="Glucose level (e.g., '95 mg/dL')")
	calcium = models.CharField(max_length=50, blank=True, help_text="Calcium level (e.g., '9.4 mg/dL')")
	sodium = models.CharField(max_length=50, blank=True, help_text="Sodium level (e.g., '140 mmol/L')")
	potassium = models.CharField(max_length=50, blank=True, help_text="Potassium level (e.g., '4.2 mmol/L')")
	chloride = models.CharField(max_length=50, blank=True, help_text="Chloride level (e.g., '102 mmol/L')")
	carbon_dioxide = models.CharField(max_length=50, blank=True, help_text="Carbon Dioxide (CO2) level (e.g., '25 mmol/L')")
	bun = models.CharField(max_length=50, blank=True, help_text="Blood Urea Nitrogen (BUN) level (e.g., '14 mg/dL')")
	creatinine = models.CharField(max_length=50, blank=True, help_text="Creatinine level (e.g., '0.9 mg/dL')")
	
	# Test metadata
	test_date = models.DateField(blank=True, null=True, help_text="Date when the metabolic panel was conducted")
	lab_name = models.CharField(max_length=255, blank=True, help_text="Name of the laboratory")
	doctor_name = models.CharField(max_length=255, blank=True, help_text="Name of the ordering physician")
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Metabolic Panel - {self.user.username}"


class LiverFunctionTest(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='liver_function_test')
	
	# Liver Function Test parameters
	total_protein = models.CharField(max_length=50, blank=True, help_text="Total Protein level (e.g., '7.0 g/dL')")
	albumin = models.CharField(max_length=50, blank=True, help_text="Albumin level (e.g., '4.5 g/dL')")
	globulin = models.CharField(max_length=50, blank=True, help_text="Globulin level (e.g., '2.5 g/dL')")
	ag_ratio = models.CharField(max_length=50, blank=True, help_text="A/G Ratio (e.g., '1.8')")
	total_bilirubin = models.CharField(max_length=50, blank=True, help_text="Total Bilirubin level (e.g., '0.8 mg/dL')")
	direct_bilirubin = models.CharField(max_length=50, blank=True, help_text="Direct Bilirubin level (e.g., '0.2 mg/dL')")
	indirect_bilirubin = models.CharField(max_length=50, blank=True, help_text="Indirect Bilirubin level (e.g., '0.6 mg/dL')")
	ast_sgot = models.CharField(max_length=50, blank=True, help_text="AST (SGOT) level (e.g., '25 U/L')")
	alt_sgpt = models.CharField(max_length=50, blank=True, help_text="ALT (SGPT) level (e.g., '30 U/L')")
	alkaline_phosphatase = models.CharField(max_length=50, blank=True, help_text="Alkaline Phosphatase level (e.g., '90 U/L')")
	ggt = models.CharField(max_length=50, blank=True, help_text="GGT level (e.g., '20 U/L')")
	
	# Test metadata
	test_date = models.DateField(blank=True, null=True, help_text="Date when the liver function test was conducted")
	lab_name = models.CharField(max_length=255, blank=True, help_text="Name of the laboratory")
	doctor_name = models.CharField(max_length=255, blank=True, help_text="Name of the ordering physician")
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Liver Function Test - {self.user.username}"


class UserNutritionGoals(models.Model):
	"""Store user's daily nutrition goals"""
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nutrition_goals')
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
	UNIT_CHOICES = [
		('g', 'grams'),
		('kg', 'kilograms'), 
		('oz', 'ounces'),
		('lb', 'pounds'),
		('cup', 'cups'),
		('ml', 'milliliters'),
		('l', 'liters')
	]
	
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_entries', null=True, blank=True)  # Link to authenticated user
	food_name = models.CharField(max_length=255)
	quantity = models.FloatField()
	unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='g')
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
		return f"{self.food_name} - {self.quantity}{self.unit}"
	
	def convert_to_grams(self):
		"""Convert quantity to grams based on unit"""
		conversion_factors = {
			'g': 1.0,
			'kg': 1000.0,
			'oz': 28.3495,
			'lb': 453.592,
			'cup': 240.0,  # Approximate for liquid
			'ml': 1.0,     # Approximate for liquid foods
			'l': 1000.0    # Approximate for liquid foods
		}
		return self.quantity * conversion_factors.get(self.unit, 1.0)
	
	def save(self, *args, **kwargs):
		# Calculate total values based on quantity converted to grams
		if self.quantity and self.calories_per_100g:
			quantity_in_grams = self.convert_to_grams()
			multiplier = quantity_in_grams / 100
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
