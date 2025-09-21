import requests
from django.conf import settings
from django.core.cache import cache

BASE = settings.WP_BASE.rstrip("/")
TTL  = getattr(settings, "WP_FRAG_CACHE_TTL", 300)

def _get_json(path: str):
    url = f"{BASE}{path}"
    headers = {"Accept": "application/json"} 
    r = requests.get(url,headers=headers, timeout=8)
    r.raise_for_status()
    return r.json()

def get_wp_header_full() -> str:
    key = "wpfrag:header_full"
    html = cache.get(key)
    if html is None:
        html = _get_json("/wp-json/theme/v1/header-full").get("html", "")
        cache.set(key, html, TTL)
    return html

def get_wp_footer_full() -> str:
    key = "wpfrag:footer_full"
    html = cache.get(key)
    if html is None:
        html = _get_json("/wp-json/theme/v1/footer-full").get("html", "")
        cache.set(key, html, TTL)
    return html
