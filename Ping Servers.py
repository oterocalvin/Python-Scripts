import subprocess
import smtplib
import encodings
import datetime
import time
from email.message import EmailMessage

#list of ips to ping#
Antennas = ['ip1', 'ip2', 'ip3', 'ip4']
currentTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M %p")

def ping():
    for a in Antennas:
        output = subprocess.Popen(["ping.exe", a], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = output.communicate()
        out = str('unreachable').encode()
        i = 0
        while i < 6:
            
            if out in stdout:
                print(a +' is unreachable trying again...')
                i += 1
                output = subprocess.Popen(["ping.exe", a], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = output.communicate()
                out = str('unreachable').encode()
            else:
                print(a + ' is online')
                break
                
        if i == 6:
            print(a + ' is offline. Sending email notification')
            user = 'sendfrom@domain.com'
            sendto = 'sendto@domain.com'
            subject = 'Antenna offline'
            body = 'this antenna is offline'
            msg = EmailMessage()
            msg['Subject'] = a + ' is offline ' + currentTime
            msg['From'] = user
            msg['To'] = sendto
            msg.set_content(a + ' is offline')

            mailserver = smtplib.SMTP('smtp.office365.com', 587)
            mailserver.ehlo()
            mailserver.starttls()
            mailserver.login('sending email here', 'password here')
            mailserver.send_message(msg)
            mailserver.close()
            i = 0

ping()

