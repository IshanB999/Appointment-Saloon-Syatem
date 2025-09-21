from django.conf import settings
from twilio.rest import Client
from urllib.parse import quote
from decouple import config

_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_whatsapp_text(to_whatsapp: str, body: str) -> str:
    """
    to_whatsapp: 'whatsapp:+9779...'
    body: plain text
    returns: Twilio Message SID
    """
    msg = _client.messages.create(
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=to_whatsapp,
        body=body,
    )
    return msg.sid


def send_booking_alert(customer_name: str, customer_phone: str, service: str, email: str | None = None) -> str:
    """
    Sends a simple admin alert: someone booked with basic customer details.
    """
    lines = [
        "✅ New appointment booking",
        f"Name: {customer_name}",
        f"Phone: {customer_phone}",
        f"Service: {service}",
    ]
    if email:
        lines.append(f"Email: {email}")
    text = "\n".join(lines)
    return send_whatsapp_text(f'whatsapp:{config("WHATS_APP_NUMBER")}', text)


def build_whatsapp_url(phone_e164: str, text: str) -> str:
    """
    phone_e164: e.g. '+9779801977302'
    Returns a wa.me URL that works on mobile and desktop (WhatsApp Web).
    """
    digits = "".join(ch for ch in phone_e164 if ch.isdigit())   # strip +, spaces, etc.
    return f"https://wa.me/{digits}?text={quote(text)}"