from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserBasicData, UserHealthProfile

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