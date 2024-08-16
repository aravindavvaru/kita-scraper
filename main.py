from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pickle
import requests
import pandas as pd
import json

session = HTMLSession()
base_url = "https://kita-navigator.berlin.de"
kita_api = "https://kita-navigator.berlin.de/api/v1/kitas"
for i in range(1, 14):
    static = "https://kita-navigator.berlin.de/einrichtungen?input=Stra%C3%9Fburger%20Str.%2C%2010405%20Berlin%2C%20Germany&betb=6-2024&einfacheSuche=true&entfernung=2&lat=52.5304792&lon=13.4143119&"
    dynamic = f"seite={i}&index=0&seite={i}"
    final = f"{static}+{dynamic}"
    r = session.get(f"{final}")
    r.html.render(wait=5)
    soup = BeautifulSoup(r.html.raw_html, "html.parser")
    kita_ids = []
    for a in soup.find_all("a", {"class": "btn btn-primary"}):
        if a.text:
            text = a["href"]
            id_pre = text.split("?")[0]
            id_final = id_pre.replace("/einrichtungen/", "")
            kita_ids.append(id_final)
    output = []
    for ids in kita_ids:
        response = requests.get(kita_api + "/" + ids)
        output = response.json()["kontaktdaten"]
        print(response.json()["kontaktdaten"]["emailadresse"])
