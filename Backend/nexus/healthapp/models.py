from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class MedicineRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=200)
    medicine_dosage = models.CharField(max_length=100)
    medicine_frequency = models.CharField(max_length=100)
    medicine_timing = models.JSONField(default=list)  # Store as JSON array
    medicine_quantity_available = models.IntegerField()
    medicine_special_instructions = models.TextField(blank=True)
    restock_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.medicine_name}"


class HealthAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alert_date = models.DateField()
    alert_time = models.TimeField()
    alert_issue_detected = models.TextField()
    alert_advice = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.alert_issue_detected[:50]}"


class LabResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lab_test_name = models.CharField(max_length=200)
    lab_date_conducted = models.DateField()
    lab_results = models.JSONField(default=dict)  # Store parameter: value pairs
    lab_normal_ranges = models.JSONField(default=dict)  # Store parameter: normal_range pairs
    interpretation_summary = models.TextField()
    interpretation_abnormalities = models.JSONField(default=list)
    recommendation_date = models.DateField()
    recommendation_action = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.lab_test_name}"


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_symptoms = models.JSONField(default=list)
    assessment_urgency_level = models.CharField(max_length=50)
    hospital_name = models.CharField(max_length=200)
    hospital_address = models.TextField()
    hospital_distance_km = models.FloatField()
    appointment_status = models.CharField(max_length=50)
    appointment_doctor = models.CharField(max_length=200)
    appointment_department = models.CharField(max_length=100)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    confirmation_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.appointment_doctor} on {self.appointment_date}"