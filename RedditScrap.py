import os
import random
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
subreddits = ["DiretoDoZapZap","Orochinho","HUEstation"]
links = []
session = HTMLSession()
request = session.get("https://www.reddit.com/r/"+subreddits[random.randint(0,len(subreddits)-1)]+"/")
soup = BeautifulSoup(request.html.html, features="lxml")
imgs = soup.findAll("img", {"alt": "Post image"})
for img in imgs:
    links.append(img['src'])
response = requests.get(links[random.randint(1,len(links)-1)])
if response.status_code == 200:
    with open(os.getcwd()+"/"+str(random.randint(1111,9999))+".jpg", 'wb') as f:
        f.write(response.content)
        print("[+] Salvo.")