import ftplib
import os

class FTP:
    def __init__(self, infos):
        if not os.path.exists("output"):
            os.makedirs("output")
        self.infos = infos

    def download(self):
        ftp = ftplib.FTP(self.infos["ip"])
        ftp.login(self.infos["user"], self.infos["mdp"])
        with open('output/' + self.infos["file_id"], 'wb') as f:
            ftp.retrbinary('RETR ' + self.infos["link"] + self.infos["file_id"], f.write)
        ftp.quit()
