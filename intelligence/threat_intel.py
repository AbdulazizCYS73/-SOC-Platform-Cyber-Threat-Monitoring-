import requests
import os 
API_KEY = os.getenv("ABUSEIPDB_KEY")

def check_ip(ip):

    url = "https://api.abuseipdb.com/api/v2/check"

    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    response = requests.get(url, headers=headers, params=params)

    return response.json()
