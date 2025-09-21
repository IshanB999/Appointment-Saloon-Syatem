from django.shortcuts import render
from system.send_whatsapp import send_free_text, check_phone_number_id
from django.http import HttpResponse
from system.send_whatsapp_twilio import send_booking_alert, build_whatsapp_url
from django.shortcuts import redirect

def send_message_view(request):
    # to = "whatsapp:+9779861155943"
    # msg = 'Hello from Django and WhatsApp!'
    # try:
    #     res = send_template(to, msg)
    #     print(res)
    #     return HttpResponse(res)
    # except Exception as e:
    #     print('error',e)
    #     return HttpResponse({'status': 'error', 'message': str(e)})
    
    # try:
    #     sid = send_booking_alert(name, phone, service, email=email)
    #     return HttpResponse({"ok": True, "sid": sid})
    # except Exception as e:
    #     print(e)
    #     # don't crash the booking if WA fails; just report/log
    #     return HttpResponse({"ok": True, "wa_error": str(e)}, status=200)
    name   = 'Niroj Prajapati'          # or data["name"]
    phone  = '861155936'
    service = 'Hair Cut'
    email  = 'nioj@gmail.com' 
    msg = (
            f"Hello! I'd like to confirm my appointment.\n"
            f"Name: {name}\n"
            f"Phone: {phone}\n"
            f"Service: {service}"
        )

    url = build_whatsapp_url('+9779861155943', msg)
    return redirect(url)
