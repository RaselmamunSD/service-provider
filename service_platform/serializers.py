import logging
import pandas as pd
from rest_framework import serializers
from service_review_v1 import settings
from accounts.models import CustomUser
from .messages import send_bulk_email,send_twilio_message
from .models import (
    ServicePlatforms,
    Platform,Campaign,
    Customer,
    CampaignMessage,
    CustomerReview,
    OnlineReview
    )


logger = logging.getLogger('django')

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id','name')
        
class ServicePlatformsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePlatforms
        fields = ('service_provider','platform','credentials')
    
    
    def to_internal_value(self, data):
        """Custom validation to check if service_provider and platform exist before default validation."""
        errors = {}

        #  Validate service_provider
        service_provider_id = data.get("service_provider")
        if not CustomUser.objects.filter(id=service_provider_id).exists():
            errors["service_provider"] = ["Service provider not found."]

        # Validate platform
        platform_id = data.get("platform")
        if not Platform.objects.filter(id=platform_id).exists():
            errors["platform"] = ["Platform not found."]

        # Raise validation error if any issue found
        if errors:
            raise serializers.ValidationError(errors)

        return super().to_internal_value(data)
    
class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'name',
            'email',
            'phone_number',
            'address',
            'is_sent_email',
            'is_given_review'
            ]

class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number', 'address']
    
class CampaignSerializer(serializers.ModelSerializer):
    
    