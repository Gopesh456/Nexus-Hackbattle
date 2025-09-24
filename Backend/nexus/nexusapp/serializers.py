from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FoodNutrition

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


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