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


