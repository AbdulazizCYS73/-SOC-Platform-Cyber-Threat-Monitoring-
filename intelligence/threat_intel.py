import os
import requests

API_KEY = os.getenv("ABUSEIPDB_KEY")
API_URL = "https://api.abuseipdb.com/api/v2/check"

def check_ip(ip):
    if not API_KEY:
        raise RuntimeError("API key missing: set ABUSEIPDB_KEY in environment")

    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    resp = requests.get(API_URL, headers=headers, params=params, timeout=10)
    resp.raise_for_status()     
    return resp.json()
