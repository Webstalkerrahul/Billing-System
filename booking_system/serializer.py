from rest_framework import serializers
from .models import Resources, Bookings
from django.db import transaction
from django.contrib.auth.models import User

class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = ('name', 'description', 'total_quantity', 'available_quantity')

class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ('user', 'resource', 'purchase_quantity', 'booking_date')
    
    def validate(self, data):
        resource = data['resource']
        purchase_quantity = data['purchase_quantity']
        
        if purchase_quantity <= 0:
            raise serializers.ValidationError("Purchase quantity must be greater than 0")
            
        if purchase_quantity > resource.available_quantity:
            raise serializers.ValidationError(
                f"Not enough available quantity. Only {resource.available_quantity} items available."
            )
        
        return data

    def create(self, validated_data):
        with transaction.atomic():
            resource = validated_data['resource']
            purchase_quantity = validated_data['purchase_quantity']
            
            resource.available_quantity -= purchase_quantity
            resource.save()
            
            booking = Bookings.objects.create(**validated_data)
            
            return booking
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']