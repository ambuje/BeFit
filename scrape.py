import requests
from bs4 import BeautifulSoup as bsa
url="https://raw.githubusercontent.com/Arjun009/WorldMap/master/rawfile"
r = requests.get(url)
if r.status_code == 200 :
    html = bsa(r.text,'html.parser');
    html=str(html).strip()
    html=html.split("\n")
    print(html)
