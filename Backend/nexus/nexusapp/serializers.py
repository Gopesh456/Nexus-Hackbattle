from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserBasicData, UserHealthProfile, BloodTestReport
from .models import FoodNutrition, UserNutritionGoals

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
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
                 'current_medications', 'blood_group', 'emergency_contact')
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
