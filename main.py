import os
import ftplib
import pandas as pd
from lib.info import infos
import matplotlib.pyplot as plt

# folder lib/ must exist
if not os.path.exists('lib/'):
    os.makedirs('lib/')

ftp = ftplib.FTP(infos["ip"])
ftp.login(infos["user"], infos["mdp"])
with open('lib/' + infos["file_id"], 'wb') as f:
    ftp.retrbinary('RETR ' + "/Disque dur/Domotique/Chaudiere/" + infos["file_id"], f.write)
ftp.quit()
df = pd.read_csv('lib/' + infos["file_id"])

cycles = df["activity"].sum()
df["timestamp"] = pd.to_datetime(df["time"], format="%Y-%m-%d %H:%M:%S")
df.drop(columns=["time"])
df["diff"] = df["timestamp"].diff().fillna(pd.Timedelta(seconds=0))
df["diff"] = df["diff"].where(df["activity"] == 0, pd.Timedelta(seconds=0))
duree_totale = df["diff"].sum()

print("## Nombre de cycles : ", cycles)
print("## Durée totale de fonctionnement : ", duree_totale)

diff = df[df["activity"] == 0]
df["hour"] = df["timestamp"].dt.hour
df["hour"] = df["hour"].astype(str)
df = df[df["activity"] == 1]
df = df.sort_values(by="hour")
df = df.drop(columns=["diff"])
df['hour'] = df['timestamp'].dt.hour
result = df.groupby('hour')['activity'].count()

print("## Durée moyenne d'un cycle : ", diff["diff"].mean())
print("## Nombre de cycles par heure :")
result.plot(kind="bar")
plt.show()