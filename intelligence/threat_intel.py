import requests

API_KEY = "5f0e5430fb506b7f8a29652273a489c34a4aa323c943ce343788504154c1dd8b697bac814ace0e29"

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