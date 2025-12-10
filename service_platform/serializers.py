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

      