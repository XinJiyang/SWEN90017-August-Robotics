# Accountmanagement/serializers.py

from rest_framework import serializers
from .models import Account
# serializers.py (or in any relevant file in your app)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['role'] = user.privilege

        return token


from django.contrib.auth.hashers import check_password

class AccountSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Account
        fields = ['username', 'password', 'new_password', 'old_password', 'privilege', 'email']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Account(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        old_password = validated_data.pop('old_password', None)
        new_password = validated_data.pop('new_password', None)

        # Check if old password is correct
        if old_password and not check_password(old_password, instance.password):
            raise serializers.ValidationError({"old_password": "Old password is not correct."})
        

        # Check if username is being changed
        if 'username' in validated_data and validated_data['username'] != instance.username:
            raise serializers.ValidationError({"username": "This field cannot be changed."})

        # Update the password if a new password is provided and the old password is correct
        if new_password and old_password and check_password(old_password, instance.password):
            instance.set_password(new_password)
            instance.save()
        else:
            raise serializers.ValidationError({"new_password": "New password is not provided or old password is not correct."})

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


