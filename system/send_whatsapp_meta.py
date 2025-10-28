import requests
from django.conf import settings
import json

PHONE_NUMBER_ID = settings.WHATSAPP_PHONE_NUMBER_ID
ACCESS_TOKEN = settings.WHATSAPP_ACCESS_TOKEN

def send_whatsapp_message(phone_number: str, message_text: str) -> dict:
    """
    Sends a WhatsApp message using Meta WhatsApp Cloud API.

    Args:
        phone_number (str): In format '977XXXXXXXXX' (without '+').
        message_text (str): The message content to send.

    Returns:
        dict: The JSON response from the WhatsApp Cloud API.
    """
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,   # dynamic number
        "type": "text",
        "text": {"body": message_text}
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        print("WhatsApp API Response:", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error sending WhatsApp message:", str(e))
        return {"error": str(e)}


def build_whatsapp_message(booking, services: list, total: float) -> str:
    service_lines = "\n".join([f"{s['name']} - NRs {s['price']}" for s in services])
    message = (
        f"Hello {booking.full_name},\n\n"
        f"Your appointment at {booking.outlet.name} is confirmed.\n\n"
        f"Date: {booking.booking_date}\n"
        f"Time: {booking.booking_time}\n\n"
        f"Services:\n{service_lines}\n\n"
        f"Total: NRs {total}\n\n"
        "Thank you for booking with us!"
    )
    return message
