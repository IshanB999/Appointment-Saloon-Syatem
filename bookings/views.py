from django.shortcuts import render, redirect
from django.http import JsonResponse
from system.send_whatsapp_meta import send_whatsapp_message, build_whatsapp_message
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def send_message_view(request):
    """
    Test WhatsApp message sending via Meta API
    """

    # Test booking data (you can replace this with real booking object later)
    booking = type('Booking', (), {})()
    booking.full_name = 'Niroj Prajapati'
    booking.outlet = type('Outlet', (), {'name': 'Neel David Salon'})()
    booking.booking_date = '2025-10-17'
    booking.booking_time = '2:00 PM'

    # Sample service data
    services = [
        {"name": "Hair Cut", "price": 500},
        {"name": "Beard Trim", "price": 300}
    ]
    total = 800

    # The recipient's WhatsApp number (must include country code, without '+')
    recipient_phone = "9779845822329"

    # Build message text
    message_text = build_whatsapp_message(booking, services, total)

    print("\n================ WHATSAPP DEBUG LOG =================")
    print("Recipient Phone:", recipient_phone)
    print("Message Text:\n", message_text)
    print("=====================================================\n")

    # Send the message
    response = send_whatsapp_message(recipient_phone, message_text)

    print("\n================ WHATSAPP API RESPONSE ================")
    print(response)
    print("======================================================\n")

    # Handle the response
    if "error" in response:
        return JsonResponse({
            "status": "failed",
            "error": response["error"]
        }, status=400)

    return JsonResponse({
        "status": "success",
        "message": "WhatsApp message sent successfully!",
        "response": response
    })
