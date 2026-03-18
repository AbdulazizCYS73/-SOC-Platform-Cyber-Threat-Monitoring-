MITRE_MAP = {

"Brute Force":"T1110",
"SQL Injection":"T1190",
"Port Scan":"T1046",
"XSS":"T1059",
"DDoS":"T1498"

}

def map_attack_to_mitre(attack):

    return MITRE_MAP.get(attack,"Unknown")