from twilio.rest import Client
import random
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Your Twilio account SID and auth token
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = '+16614854698'
my_phone_number = '+917507994393'

print(f'len(account_sid) = {len(account_sid)}')
print(f'len(auth_token) = {len(auth_token)}')
print(f'twilio_phone_number = {twilio_phone_number}')

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Function to send OTP via Twilio
def send_otp(my_phone_number):
    otp = generate_otp()
    message_body = f'Your OTP is: {otp}'

    try:
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,  # Your Twilio phone number
            to=my_phone_number  # Recipient's phone number
        )
        print(f"OTP sent successfully to {my_phone_number}")
    except Exception as e:
        print(f"Failed to send OTP: {e}")

# Example usage
if __name__ == "__main__":
    send_otp(my_phone_number)
