import requests
import json

# Razorpay API credentials
RAZORPAY_KEY_ID = 'rzp_test_7DsJGQPeYoXK0N'
RAZORPAY_KEY_SECRET = 'cmwhT5lOuC2zINSqg66xhwCR'

# Endpoint for creating a payment link
url = 'https://api.razorpay.com/v1/payment_links'

# Payment link details
data = {
    'amount': 500,  # Amount in paise (e.g., ₹500.00)
    'currency': 'INR',
    'accept_partial': False,
    'description': 'Payment for Order #12345',
    'customer': {
        'name': 'Yash Potdar',
        'email': 'yash@bnbdevelopers.in',
        'contact': '+919876543210'
    },
    'notify': {
        'sms': False,
        'email': False
    },
    'reminder_enable': False,
    'notes': {
        'order_id': '12345',
        'hall_type': 'conf_hall',
        'time':"11:00-1:00",
        'date':"23/03/2025"
    },
    'callback_url': 'https://yourwebsite.com/payment/callback',
    'callback_method': 'get'
}

# Make the request
response = requests.post(url, auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET), data=json.dumps(data), headers={'Content-Type': 'application/json'})

# Check the response
if response.status_code == 200:
    payment_link = response.json()['short_url']
    print(f'Payment link created successfully: {payment_link}')
else:
    print(f'Failed to create payment link: {response.text}')
