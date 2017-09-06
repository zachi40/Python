# -*- coding: utf-8 -*-
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

EMAIL_FROM = 'Your name<Your mail>'
EMAIL_TO = ['send to']
SUBJECT = ''
MESS = '<html dir="rtl" xmlns="http://www.w3.org/1999/xhtml"><body>Your msg in html</body></html>'
BODY = MIMEText(MESS,'html', 'utf-8')
FILE_TO_ATT = 'file location'

#Setting attachmint
part = MIMEBase('application', 'octet-stream')
part.set_payload(open(FILE_TO_ATT, 'rb').read())
Encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="%s"'%(os.path.basename(FILE_TO_ATT)))

#Setting Message
msg = MIMEMultipart()
msg['Subject'] = SUBJECT
msg['From'] = EMAIL_FROM
msg['To'] = ', '.join(EMAIL_TO)

msg.attach(BODY)
msg.attach(part)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('Gmail username', 'gmail pass')
server.sendmail(EMAIL_FROM, EMAIL_TO,msg.as_string())
server.quit()