import os
import ftplib
import pandas as pd
from lib.info import infos
import matplotlib.pyplot as plt

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

print("- Number of cycles:", cycles)
print("- Total operation time:", duree_totale.strftime("%H:%M:%S"))

diff = df[df["activity"] == 0]
print("- Average cycle duration: ", diff["diff"].mean().strftime("%H:%M:%S"))

df["hour"] = df["timestamp"].dt.hour
df["day"] = df["timestamp"].dt.day

df2 = df.groupby(["day", "hour"]).count()
df2 = df2["activity"]
df2 = df2.reset_index()
df2 = df2["activity"].groupby(df2["hour"]).mean()
df2.plot(kind="bar", title="Moyenne d'activité par heure", xlabel="Heure", ylabel="Nombre de cycles", color="blue", alpha=0.5)
for i in df2.index:
    plt.text(i, df2[i], str(round(df2[i], 2)), ha="center", va="bottom")
plt.show()