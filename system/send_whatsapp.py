# system/send_whatsapp.py
from decouple import config
import requests

PHONE_NUMBER_ID = config("whats_app_phone_id")
ACCESS_TOKEN    = config("whats_app_access_token")
BASE_URL = "https://graph.facebook.com/v20.0"

def _headers():
    return {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}

def check_phone_number_id():
    r = requests.get(
        f"{BASE_URL}/{PHONE_NUMBER_ID}",
        params={"fields": "id,display_phone_number"},
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}, timeout=20
    )
    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}
    return r.status_code, data    

def send_template(to_e164: str, name="hello_world", lang="en_US", components=None):
    url = f"{BASE_URL}/{PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to_e164,
        "type": "template",
        "template": {"name": name, "language": {"code": lang}},
    }
    if components:
        payload["template"]["components"] = components
    r = requests.post(url, headers=_headers(), json=payload, timeout=20)
    if r.status_code >= 400:
        raise RuntimeError(f"send_template {r.status_code}: {r.text}")
    return r.json()

def send_free_text(to_e164: str, body: str, retry_if_closed=True):
    url = f"{BASE_URL}/{PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to_e164,
        "type": "text",
        "text": {"preview_url": False, "body": body},
    }
    r = requests.post(url, headers=_headers(), json=payload, timeout=20)
    print(r)
    if r.status_code < 400:
        return r.json()

    # Inspect error for closed window
    try:
        err = r.json()
    except Exception:
        err = {"raw": r.text}

    # If no customer service window, open with template and retry once
    code = (
        err.get("error", {}).get("code"),
        err.get("error", {}).get("error_subcode"),
        err.get("error", {}).get("message", ""),
    )
    closed_window = "no customer service window" in str(err).lower() or "131047" in str(err)

    if retry_if_closed and closed_window:
        send_template(to_e164, name="hello_world")
        return send_free_text(to_e164, body, retry_if_closed=False)

    raise RuntimeError(f"send_free_text {r.status_code}: {err}")
