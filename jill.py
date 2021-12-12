import discord, time, logging, threading, requests, asyncio
from bs4 import BeautifulSoup
import random
from datetime import datetime, timezone

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

PRODUCT = "jill-plush/"
_READY = False

@client.event
async def on_ready():
	global _READY
	_READY = True
	await client.change_presence(activity=discord.Activity(name="VA-11 Hall-A: Cyberpunk Bartender Action", type=0))

REQID = 46068

async def RunScraper():
	global PRODUCT, client, _READY, REQID
	while not _READY:
		await asyncio.sleep(0.1)
	print("[jill] Started loop of Scraper.")
	_notif = client.get_channel(819073622105653299)
	_rules = client.get_channel(819114956883886100)
	_msgUp = await _rules.fetch_message(847189790398873630)
	_plushURL = "https://merch.ysbryd.net/products/"+PRODUCT
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
			print(_a)
			if not _a == "Unavailable":
				await _notif.send("(no more ping)\n Jill Plush is Available!\n<https://merch.ysbryd.net/products/jill-plush>")
			now = datetime.now(timezone.utc)
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
			await _msgUp.edit(content = "Last fetch : "+dt_string+" (UTC)\nResponse: `"+str(_a)+"`\nThis session updates: `"+str(REQID)+"`\n\nIf time is more than 5 minute late the bot is down.")
			await asyncio.sleep(65)
		except Exception as e:
			print("[jill] Exception caught. Restarting...")
			print(str(e))
			time.sleep(0.3)
			await RunScraper()

client.loop.create_task(RunScraper())
client.run("")