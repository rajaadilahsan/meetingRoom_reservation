from dataclasses import fields
from rest_framework import serializers
from .models import employees, rooms, reservation, reservationInvitees
from django.contrib.auth.models import User

class employeesSerializer(serializers.ModelSerializer):

    class Meta:
        model=employees
  #      fields=('firstname','lastname')
        fields='__all__'


class roomsSerializer(serializers.ModelSerializer):

    class Meta:
        model=rooms
        fields='__all__'



class reservationInviteesSerializer(serializers.ModelSerializer):

    class Meta:
        model=reservationInvitees
        fields='__all__'


class reservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=reservation
        fields='__all__'

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user



