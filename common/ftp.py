import ftplib
import os

class FTP:
    def __init__(self, passwd, user, ip, link, file_id):
        if not os.path.exists("output"):
            os.makedirs("output")
        self.infos = {
            "ip": ip,
            "user": user,
            "mdp": passwd,
            "link": link,
            "file_id": file_id
        }

    def download(self):
        ftp = ftplib.FTP(self.infos["ip"])
        ftp.login(self.infos["user"], self.infos["mdp"])
        with open('output/' + self.infos["file_id"], 'wb') as f:
            ftp.retrbinary('RETR ' + self.infos["link"] + self.infos["file_id"], f.write)
        ftp.quit()
