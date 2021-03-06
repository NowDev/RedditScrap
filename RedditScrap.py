import os
from os import path
import re
import random

#Use: pip installl bealtifulsoup4
from bs4 import BeautifulSoup
#Use: pip install requests-html
from requests_html import HTMLSession
#Use: pip installl requests
import requests

#Put the subreddits that you want
subreddits = ["DiretoDoZapZap","Orochinho","HUEstation"]

def formatar(filename):
    for caractere in ['\\',' ','*','/','\'','\"','?','!',':','|','<','>','*',')','(','+','~','.']:
        if caractere in filename:
            filename = filename.replace(caractere,"")
    return filename

def download():

    #Arrays of post links and titles
    links = []
    titles = []
    #Our session
    session = HTMLSession()
    #Select a random subreddit of the array "subreddits"
    sub = str(subreddits[random.randint(0,len(subreddits)-1)])

    print("[+] Downloading from r/" + sub)
    request = session.get("https://www.reddit.com/r/"+sub+"/")
    soup = BeautifulSoup(request.html.html, features="lxml")

    imgs = soup.findAll("img", {"alt": "Post image"})
    for img in imgs:
        links.append(img["src"])

    title = soup.findAll("h3","_eYtD2XCVieq6emjKBH3m")
    for titleraw in title:
        s = str(titleraw)
        s = s.replace("<h3 class=\"_eYtD2XCVieq6emjKBH3m\">","")
        s = s.replace("</h3>","")
        titles.append(s)

    print("[+] Found " + str(len(links)) + " link(s).")

    # if our request don't find links...
    if(len(links)<1):
        print("[!] Error downloading from r/"+sub+", does this sub exists?")
        exit()
    link = random.randint(1,len(links))
    filename = formatar(str(titles[link+1].lower()))
    
    # added -1 when getting arrays because *i* forgot that arrays start on 0 and not on 1, lol
    response = requests.get(str(links[link-1]))
    if response.status_code == 200:
        if path.exists(os.getcwd()+"/"+filename+".jpg"):
            print("[!] Existent file, trying again...\n")
            del links
            del titles
            response.close()
            session.close()
            download()
            return
        else:    
            with open(os.getcwd()+"/"+filename+".jpg", 'wb') as f:
                f.write(response.content)
                print("[+] downloaded (" + os.getcwd()+"/"+filename+".jpg)\n[>] Link: " + str(links[link]) + "\n[>] Title: " + str(titles[link+1])+"\n")

download()