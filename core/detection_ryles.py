def detect_bruteforce(df):

    alerts = []

    ip_counts = df["ip"].value_counts()

    for ip,count in ip_counts.items():

        if count > 3:

            alerts.append({
                "type":"Brute Force",
                "ip":ip,
                "severity":"High"
            })

    return alerts