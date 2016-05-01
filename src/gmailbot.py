# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 13:30:51 2016

@author: dk
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

fromaddr = 'plagueratbot@gmail.com'
toaddrs  = 'dstryrk@yahoo.com'
msg = 'Ratbot speaks!'
SUBJECT = 'Ratbot backup #familystuff'
userlist= ['dstryrk@yahoo.com','matt.dimmic@gmail.com','jay.mukid@gmail.com']
testlist= ['dstryrk@yahoo.com']

# Credentials (if needed)
username = 'plagueratbot'

#TODO add config
password = '********'

with open("C:\Users\dk\Desktop\Ratbot\\html\\familystuff.html",'r') as fh:
    html = fh.read()

msg = MIMEMultipart('alternative')
msg['Subject'] = "Ratbot is alive"
msg['From'] = toaddrs
part = MIMEText(html, 'html')
msg.attach(part)

for user in userlist:
# The actual mail send
    msg['To'] = user    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, user,  msg.as_string())
    server.quit()
    
# Create message container - the correct MIME type is multipart/alternative.

#msg['Subject'] = "Link"
#msg['From'] = me
#msg['To'] = you

'''
# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="https://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Send the message via local SMTP server.
s = smtplib.SMTP('localhost')
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.sendmail(me, you, msg.as_string())
s.quit()

'''