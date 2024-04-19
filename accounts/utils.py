import requests
from django.conf import settings


def send_otp(mobile, otp):
    """
    Send message.
    """
    # url = f"https://2factor.in/API/V1/{settings.SMS_API_KEY}/SMS/{mobile}/{otp}/Your OTP is"
    url = f"https://sms.flaminqocloud.com/api/v2/send.php?user_id=105529&api_key=vc2o7sts4fawhuuta&sender_id=Flaminqo&to=788575120&message=test"
    payload = ""
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.get(url, data=payload, headers=headers)
    return bool(response.ok)
