import discord, time, logging, threading, requests, asyncio
from bs4 import BeautifulSoup
import random

from settings import *

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()
_READY = False

@client.event
async def on_ready():
	global _READY
	_READY = True
	await client.change_presence(activity=discord.Activity(name="VA-11 Hall-A: Cyberpunk Bartender Action", type=0))

REQID = 0

State = "Unavailable"

async def RunScraper():
	global PRODUCT, client, _READY, REQID, State
	while not _READY:
		await asyncio.sleep(0.1)
	print("[jill] Started loop of Scraper.")
	_notif = client.get_channel(CHANNEL_ID)
	_plushURL = "https://merch.ysbryd.net/products/"+PRODUCT+"/"
	while True:
		try:
			_plush = requests.get(_plushURL+"?_="+str(random.randint(1,1000000)))
			try:
				soup = BeautifulSoup(_plush.text, 'html.parser')
			except:
				print("[jill] Error parsing.")
			print("[jill] Request #"+str(REQID)+" ... ", end="")
			REQID += 1
			_a = soup.find("button", {"id": "addToCart-product-template"})
			_a = _a.text.replace(" ", "").replace("\n", "")

			if not _a == "Unavailable" and State == "Unavailable":
				await _notif.send(CUSTOM_MESSAGE)

			if State != _a:
				State = _a
			
			await asyncio.sleep(DELAY)
		except Exception as e:
			print("[jill] Exception caught. Restarting...")
			print(str(e))
			time.sleep(0.3)
			await RunScraper()

client.loop.create_task(RunScraper())
client.run(CLIENT_TOKEN)