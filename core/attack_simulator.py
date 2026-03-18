import random
from datetime import datetime

countries=["Russia","China","USA","Germany","Iran"]

attacks=["Brute Force","SQL Injection","Port Scan","DDoS","XSS"]

def simulate_attack():

    return {

        "time":datetime.now().strftime("%H:%M:%S"),

        "ip":f"192.168.1.{random.randint(1,200)}",

        "country":random.choice(countries),

        "attack_type":random.choice(attacks),

        "risk":"High",

        "lat":random.randint(-60,60),

        "lon":random.randint(-120,120)

    }