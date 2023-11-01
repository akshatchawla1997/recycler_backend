import requests
from django.conf import settings
from django.conf import settings

# from datetime import datetime, timedelta

def send_otp(mobile, otp):
    """
    Send message.
    """
#     template_id=""
#     url = f"https://control.msg91.com/api/v5/otp?mobile={mobile}&template_id={template_id}"
#     payload = ""
#     headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     "authkey": "395570ANVDem2O0o64ddd0c6P1"
# }
#     response = requests.post(url, json=payload, headers=headers)
#     return response.text
