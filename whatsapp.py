from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
MILKMAN_NUMBER = os.getenv("MILKMAN_NUMBER")
FRIEND_NUMBER = os.getenv("FRIEND_NUMBER")
MY_NUMBER = os.getenv("MY_NUMBER")

# Function to send a WhatsApp message using Twilio
def send_whatsapp_message(quantity, date):
    """Send a WhatsApp message using Twilio API."""

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    milkman_message = (
        f"Delivered {quantity} L of Milk on {date} in 5017 Estancia\n"  # English
        f"{quantity} L பால் {date} அன்று 5017 Estancia இல் வழங்கப்பட்டது"  # Tamil
    )

    # Message for the friend (English only)
    friend_message = f"Delivered {quantity} L of Milk on {date} in 5017 Estancia"


    # Send message to the milkman
    # client.messages.create(
    #    body=milkman_message,
    #    from_=TWILIO_WHATSAPP_NUMBER,
    #    to=MILKMAN_NUMBER
    #)

    # Send message to the friend
    #client.messages.create(
    #    body=friend_message,
    #    from_=TWILIO_WHATSAPP_NUMBER,
    #    to=FRIEND_NUMBER
    #)

    client.messages.create(
        body=friend_message,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=MY_NUMBER
    )