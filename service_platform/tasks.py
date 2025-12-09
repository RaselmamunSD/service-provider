import logging
import re
from accounts.models import CustomUser
from django.db.models import Prefetch
from django.http import JsonResponse
from django.conf import settings
from celery import shared_task
from service_platform.models import ServicePlatforms
from .utils.wextractor_service  import (
    fetch_and_save_reviews_facebook,
    get_platform_users,
    # fetch_and_save_reviews_booking,
    fetch_and_save_reviews,
    get_platform,
    extract_page_id
)



logger = logging.getLogger('django')

@shared_task
def facebook_page_review():
    PLATFORM_NAME = 'facebook'
    users = get_platform_users(PLATFORM_NAME)    
    for user in users:
        try:
            # Get the latest service platform for the user and specific platform
            service_platform = get_platform(user,PLATFORM_NAME)
            page_link = service_platform.platform_link
            print(page_link,"PAGE LINK")
            page_id = extract_page_id('facebook',page_link)
            
            if not page_id:
                logger.exception("Failed to fetch page id",user,service_platform)
                continue
            
            fetch_and_save_reviews_facebook(service_platform,page_id)
        except Exception as e:
            logger.info(f"Faild to Fetch Review from Facebook for User {user}",e)
            continue

    return print("Facebook Page Review Fetch success")
  

@shared_task
def booking_dot_com_review():
    PLATFORM_NAME = 'booking'
    auth_token = settings.WEXTRACTOR_API_KEY

    users = get_platform_users(PLATFORM_NAME)
    for user in users:
        service_platform = get_platform(user,PLATFORM_NAME)
        page_link = service_platform.platform_link
        
        page_id = extract_page_id(PLATFORM_NAME,page_link)
        if not page_id:
            logger.exception("Failed to fetch page id",user,service_platform)
            continue

        WEXTRACTOR_BOOKING_API = "https://wextractor.com/api/v1/reviews/booking"
        PLATFORM_URL =  f"https://wextractor.com/api/v1/reviews/booking?id={page_id}&auth_token={auth_token}"
        
        fetch_and_save_reviews(WEXTRACTOR_BOOKING_API,PLATFORM_URL,service_platform,page_id)
        print(f"successfully fetch review user:{user}")
    return print("Successfully fetch booking.com review")
    


