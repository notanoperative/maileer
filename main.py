from bs4 import BeautifulSoup
import requests 
import re
import smtplib
from email.mime.multipart import MIMEMultipart as Mpart
from email.mime.text import MIMEText as Mtxt

def send_mail(email):
    f = open('CREDENTIALS.txt','r')
    linhas = f.readlines()
    f.close()
    host='smtp.host.etc.etc'
    port='587'
    login=linhas[0]
    senha=linhas[1]

    server = smtplib.SMTP(host,port)
    server.ehlo()
    server.starttls()

    server.login(login, senha)

    f = open('msg.txt','r')
    body = f.readlines()
    f.close()

    mail_msg = Mpart()
    mail_msg['From'] = login
    mail_msg['To'] = email
    mail_msg['Subject'] = 'Crack'
    mail_msg.attach(Mtxt(str(body), 'plain'))

    server.sendmail(mail_msg['From'],mail_msg['To'], mail_msg.as_string())

    server.quit()

BASE_URL = "https://agazetaempregos.com.br"

conn = requests.get(f'{BASE_URL}/index.php/empregos').content
bs = BeautifulSoup(conn, 'html.parser')

links=bs.select(".magazine-category-title > a")
emails =set()
for link in links:
    conn = requests.get(f'{BASE_URL}{link.get("href")}').content
    bs = BeautifulSoup(conn, 'html.parser')
    pag_empregos = bs.select('.page-header>h2>a')
    for i in pag_empregos:
        conn = requests.get(f'{BASE_URL}{i.get("href")}').content
        bs = BeautifulSoup(conn, 'html.parser')

        email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", bs.text)
        if email:
            send_mail(email[0])
            print(f'Enviado para {email[0]}')



