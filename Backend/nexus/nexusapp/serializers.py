from rest_framework import serializers
from .models import User, UserBasicData

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

class UserBasicDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBasicData
        fields = ('full_name', 'date_of_birth', 'gender', 'location', 'email', 'phone')
        read_only_fields = ('user',)