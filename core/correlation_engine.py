def detect_attack_chain(df):

    alerts = []

    for ip in df["ip"].unique():

        logs = df[df["ip"] == ip]

        if "Port Scan" in logs["attack_type"].values and "Brute Force" in logs["attack_type"].values:

            alerts.append({
                "ip":ip,
                "chain":"Recon → Brute Force",
                "severity":"Critical"
            })

    return alerts