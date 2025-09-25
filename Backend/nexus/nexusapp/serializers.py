from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserBasicData, UserHealthProfile, BloodTestReport, MetabolicPanel, LiverFunctionTest, MedicationDetails
from .models import FoodNutrition, UserNutritionGoals, Appointment, LabReport

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class UserBasicDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBasicData
        fields = ('full_name', 'date_of_birth', 'gender', 'location', 'email', 'phone')
        read_only_fields = ('user',)

class UserHealthProfileSerializer(serializers.ModelSerializer):
    emergency_contact = serializers.SerializerMethodField()
    
    class Meta:
        model = UserHealthProfile
        fields = ('height_cm', 'weight_kg', 'chronic_conditions', 'allergies', 
                 'current_medications', 'blood_group', 'daily_calorie_goal', 'daily_protein_goal', 'emergency_contact')
        read_only_fields = ('user',)
    
    def get_emergency_contact(self, obj):
        return {
            "name": obj.emergency_contact_name,
            "relationship": obj.emergency_contact_relationship,
            "phone": obj.emergency_contact_phone
        }
    
    def create(self, validated_data):
        # Handle emergency_contact nested data
        emergency_contact = validated_data.pop('emergency_contact', {})
        if emergency_contact:
            validated_data['emergency_contact_name'] = emergency_contact.get('name', '')
            validated_data['emergency_contact_relationship'] = emergency_contact.get('relationship', '')
            validated_data['emergency_contact_phone'] = emergency_contact.get('phone', '')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Handle emergency_contact nested data
        emergency_contact = validated_data.pop('emergency_contact', {})
        if emergency_contact:
            validated_data['emergency_contact_name'] = emergency_contact.get('name', instance.emergency_contact_name)
            validated_data['emergency_contact_relationship'] = emergency_contact.get('relationship', instance.emergency_contact_relationship)
            validated_data['emergency_contact_phone'] = emergency_contact.get('phone', instance.emergency_contact_phone)
        return super().update(instance, validated_data)


class BloodTestReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodTestReport
        fields = (
            'hemoglobin', 'hematocrit', 'wbc_count', 'rbc_count', 'platelet_count',
            'mcv', 'mch', 'mchc', 'neutrophils', 'lymphocytes', 'monocytes', 
            'eosinophils', 'basophils', 'test_date', 'lab_name', 'doctor_name'
        )
        read_only_fields = ('user',)


class MetabolicPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetabolicPanel
        fields = (
            'glucose', 'calcium', 'sodium', 'potassium', 'chloride', 
            'carbon_dioxide', 'bun', 'creatinine', 'test_date', 'lab_name', 'doctor_name'
        )
        read_only_fields = ('user',)


class LiverFunctionTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiverFunctionTest
        fields = (
            'total_protein', 'albumin', 'globulin', 'ag_ratio', 'total_bilirubin',
            'direct_bilirubin', 'indirect_bilirubin', 'ast_sgot', 'alt_sgpt', 
            'alkaline_phosphatase', 'ggt', 'test_date', 'lab_name', 'doctor_name'
        )
        read_only_fields = ('user',)


class MedicationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationDetails
        fields = (
            'medicine_name', 'frequency', 'medical_condition', 'no_of_pills',
            'next_order_date', 'meds_reminder'
        )
        read_only_fields = ('user',)


class FoodNutritionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = FoodNutrition
        fields = '__all__'
        read_only_fields = ('user', 'username', 'total_calories', 'total_protein', 'total_carbs', 
                          'total_fat', 'total_fiber', 'total_sugar', 'created_at')


class FoodInputSerializer(serializers.Serializer):
    food_name = serializers.CharField(max_length=255)
    quantity = serializers.FloatField(min_value=0.1)
    unit = serializers.ChoiceField(choices=[
        ('g', 'grams'),
        ('kg', 'kilograms'), 
        ('oz', 'ounces'),
        ('lb', 'pounds'),
        ('cup', 'cups'),
        ('ml', 'milliliters'),
        ('l', 'liters')
    ], default='g')
    time = serializers.TimeField(required=False, help_text="Time in HH:MM format (e.g., '08:30')")
    meal_type = serializers.ChoiceField(choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack')
    ], required=False)


class NutritionResponseSerializer(serializers.Serializer):
    food_name = serializers.CharField()
    quantity = serializers.FloatField()
    nutrition_data = serializers.DictField()
    total_nutrition = serializers.DictField()


class UserNutritionGoalsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserNutritionGoals
        fields = [
            'id', 'username', 'daily_calories_goal', 'daily_protein_goal',
            'daily_carbs_goal', 'daily_fat_goal', 'daily_fiber_goal',
            'daily_sugar_goal', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'username', 'created_at', 'updated_at']


class DailyNutritionSummarySerializer(serializers.Serializer):
    """Serializer for daily nutrition summary with goals"""
    date = serializers.DateField()
    consumed = serializers.DictField()
    goals = serializers.DictField()
    progress = serializers.DictField()
    entries_count = serializers.IntegerField()


class AppointmentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'username', 'appointment_date', 'location', 'doctor_name',
            'doctor_specialization', 'appointment_type', 'reason', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'username', 'created_at', 'updated_at']


class LabReportSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    file_size_mb = serializers.SerializerMethodField(read_only=True)
    is_image = serializers.SerializerMethodField(read_only=True)
    is_pdf = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = LabReport
        fields = [
            'id', 'username', 'report_name', 'report_type', 'lab_name', 'doctor_name',
            'report_date', 'report_file_base64', 'file_name', 'file_type', 'file_size',
            'file_size_mb', 'is_image', 'is_pdf', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'username', 'file_size_mb', 'is_image', 'is_pdf', 'created_at', 'updated_at']
    
    def get_file_size_mb(self, obj):
        return obj.get_file_size_mb()
    
    def get_is_image(self, obj):
        return obj.is_image()
    
    def get_is_pdf(self, obj):
        return obj.is_pdf()


class LabReportUploadSerializer(serializers.Serializer):
    """Serializer for lab report file upload with base64 data"""
    report_name = serializers.CharField(max_length=255)
    report_type = serializers.ChoiceField(choices=LabReport.LAB_REPORT_TYPE_CHOICES)
    lab_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    doctor_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    report_date = serializers.DateField()
    file_data = serializers.CharField(help_text="Base64 encoded file data")
    file_name = serializers.CharField(max_length=255, help_text="Original filename")
    file_type = serializers.CharField(max_length=10, help_text="File extension (e.g., pdf, jpg, png)")
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_file_data(self, value):
        """Validate base64 data"""
        import base64
        try:
            # Try to decode the base64 data to validate it
            decoded_data = base64.b64decode(value)
            # Check file size (limit to 10MB)
            if len(decoded_data) > 10 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 10MB")
            return value
        except Exception:
            raise serializers.ValidationError("Invalid base64 data")
    
    def validate_file_type(self, value):
        """Validate file type"""
        allowed_types = ['pdf', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'doc', 'docx']
        if value.lower() not in allowed_types:
            raise serializers.ValidationError(f"File type '{value}' is not allowed. Allowed types: {', '.join(allowed_types)}")
        return value.lower()
