from django.test import TestCase
import requests

# import geopy
# Create your tests here.

import urllib.parse
auth_key = "IQkJfqxEfD5l3qCu"
sender_id = "TRYGON"
route = 2
number = "9973884727"
message = "Dear armuu 1005 is the OTP for your login at Trygon. In case you have not requested this, please contact us at info@trygon.in"
template_id = "1707162192151162124"
url = f"http://weberleads.in/http-tokenkeyapi.php?authentic-key={auth_key}&senderid={sender_id}&route={route}&number={number}&message={urllib.parse.quote(message)}&templateid={template_id}"
response = requests.get(url)

if response.ok:
    print("SMS message sent successfully")
else:
    print("Error sending SMS message")
