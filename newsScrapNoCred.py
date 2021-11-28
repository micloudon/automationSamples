from decouple import config
import requests

from bs4 import BeautifulSoup

import smtplib 

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime

now = datetime.datetime.now()

content = ''

def extactNews(url):
    print("extacting hacker news stories")
    cnt = ""
    cnt += ('<b>Hacker News top stories</b>\n' + '<b>'+ '-' *50+ '</b>')
    responce = requests.get(url)
    content = responce.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title' , 'valine': ''})):
        cnt += ((str(i+1) + " :: " + tag.text + "\n" + '<br>') 
        if tag.text !="More"
        else '')
    
    return cnt

cnt = extactNews("https://news.ycombinator.com/")
content += cnt
content += ('<br>--------<br>') 
content += ('<br><br> end of message') 


# Lets send the email

print("Composing Email...")

# Update email details

SERVER = 'smtp.gmail.com' # your smtp server
PORT = 587 # Your port number
FROM = config('EMAIL') # your email id
TO = config('EMAIL') # your email ids
PASS = config('PASS') 


msg = MIMEMultipart()

msg['Subject'] = 'Top News Stories in Hacker News [Automated Email]' + str(
    now.day) + '-' + str(
    now.month) + '-' + str(
    now.year)

msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print("initiating server...")

server = smtplib.SMTP(SERVER, PORT)

server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print("Email sent...")

server.quit()
