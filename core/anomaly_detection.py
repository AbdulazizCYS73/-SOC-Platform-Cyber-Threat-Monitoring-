from sklearn.ensemble import IsolationForest

def detect_anomalies(df):

    df["ip_num"] = df["ip"].apply(lambda x: sum([int(i) for i in x.split(".")]))

    model = IsolationForest(contamination=0.2)

    model.fit(df[["ip_num"]])

    df["anomaly"] = model.predict(df[["ip_num"]])

    return df