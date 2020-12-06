import requests
from bs4 import BeautifulSoup
import re
import time
import discord
import aiohttp
from discord import Webhook, RequestsWebhookAdapter

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
def findWord(URL, palabra):
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # producto = soup.find(attrs={'class': 'ProductItem__Info'})
    producto = soup.body.find_all(string=re.compile(r'.*{0}.*'.format(palabra), re.IGNORECASE), recursive=True)
    cantidad = len(producto)
    # print (f'Found the word "{palabra}" {cantidad} times\n')
    print("Sign encontrado: " + str(cantidad) + " veces en " + URL)
    if cantidad > 0:
        sendDiscordMessage(URL)

def findWordClass(URL, palabra, clase, clase2):
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    producto = soup.find(attrs={"class": clase})
    
    cantidad = len(producto)

    for unidad in producto.find_all(attrs={"class": clase2}):
        titulo = unidad.get_text().lower()
        if titulo.find(palabra) != -1 and titulo.find("sold out") == -1:
            print("Stock")
            sendDiscordMessage(URL)
        else:
            print("Sin stock")
            sendDiscordMessage(URL)
    print("Sign encontrado: " + str(cantidad) + " veces en " + URL)

def sendDiscordMessage(URL):
    webhook = Webhook.from_url("https://discord.com/api/webhooks/781566770661818368/iUP2KNJ6DUpcgejKL9XbLQb5Ums4YA2AV0COGSIAkiLhYXzIrSeID8AaQcHCZwbX-JvU", adapter=RequestsWebhookAdapter())
    webhook.send(f"@everyone Artículo firmado publicado en {URL}")
    print("Mensaje enviado")

while True:
    findWord("https://store.taylorswift.com/", "signed")
    findWordClass("https://shop.arianagrande.com/", "signed", "product-container clearfix", "product-details")
    time.sleep(30)