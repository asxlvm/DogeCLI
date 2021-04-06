from dogehouse import DogeClient, event, command
from dogehouse.entities import User, Message, UserPreview, BaseUser, Context
import dogehouse # dogehouse.py library to make things easier ;)
import asyncio # for sleeping
import json # for settings
import datetime # just for elapsed til start
from colorama import Fore, Back, Style, init # coOlOoOrS
from concurrent.futures.thread import ThreadPoolExecutor # for asynchronous input()
import os # getting settings, clearing console, and getting the token from env

starttime = datetime.datetime.now() # for elapsed
# ascii art for every menu

DOGECLIASCII = """
▓█████▄  ▒█████    ▄████ ▓█████     ▄████▄   ██▓     ██▓
▒██▀ ██▌▒██▒  ██▒ ██▒ ▀█▒▓█   ▀    ▒██▀ ▀█  ▓██▒    ▓██▒
░██   █▌▒██░  ██▒▒██░▄▄▄░▒███      ▒▓█    ▄ ▒██░    ▒██▒
░▓█▄   ▌▒██   ██░░▓█  ██▓▒▓█  ▄    ▒▓▓▄ ▄██▒▒██░    ░██░
░▒████▓ ░ ████▓▒░░▒▓███▀▒░▒████▒   ▒ ▓███▀ ░░██████▒░██░
 ▒▒▓  ▒ ░ ▒░▒░▒░  ░▒   ▒ ░░ ▒░ ░   ░ ░▒ ▒  ░░ ▒░▓  ░░▓  
 ░ ▒  ▒   ░ ▒ ▒░   ░   ░  ░ ░  ░     ░  ▒   ░ ░ ▒  ░ ▒ ░
 ░ ░  ░ ░ ░ ░ ▒  ░ ░   ░    ░      ░          ░ ░    ▒ ░
   ░        ░ ░        ░    ░  ░   ░ ░          ░  ░ ░  
 ░                                 ░
"""
CREDITSASCII = """
 ▄████▄   ██▀███  ▓█████ ▓█████▄  ██▓▄▄▄█████▓  ██████ 
▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀ ▒██▀ ██▌▓██▒▓  ██▒ ▓▒▒██    ▒ 
▒▓█    ▄ ▓██ ░▄█ ▒▒███   ░██   █▌▒██▒▒ ▓██░ ▒░░ ▓██▄   
▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄ ░▓█▄   ▌░██░░ ▓██▓ ░   ▒   ██▒
▒ ▓███▀ ░░██▓ ▒██▒░▒████▒░▒████▓ ░██░  ▒██▒ ░ ▒██████▒▒
░ ░▒ ▒  ░░ ▒▓ ░▒▓░░░ ▒░ ░ ▒▒▓  ▒ ░▓    ▒ ░░   ▒ ▒▓▒ ▒ ░
  ░  ▒     ░▒ ░ ▒░ ░ ░  ░ ░ ▒  ▒  ▒ ░    ░    ░ ░▒  ░ ░
░          ░░   ░    ░    ░ ░  ░  ▒ ░  ░      ░  ░  ░  
░ ░         ░        ░  ░   ░     ░                 ░  
░                         ░                            
"""
PROFILEASCII = """
 ██▓███   ██▀███   ▒█████    █████▒██▓ ██▓    ▓█████ 
▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒▓██   ▒▓██▒▓██▒    ▓█   ▀ 
▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒▒████ ░▒██▒▒██░    ▒███   
▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░░▓█▒  ░░██░▒██░    ▒▓█  ▄ 
▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░░▒█░   ░██░░██████▒░▒████▒
▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░  ▒ ░   ░▓  ░ ▒░▓  ░░░ ▒░ ░
░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░  ░      ▒ ░░ ░ ▒  ░ ░ ░  ░
░░         ░░   ░ ░ ░ ░ ▒   ░ ░    ▒ ░  ░ ░      ░   
            ░         ░ ░          ░      ░  ░   ░  ░
"""
ROOMSASCII = """
 ██▀███   ▒█████   ▒█████   ███▄ ▄███▓  ██████ 
▓██ ▒ ██▒▒██▒  ██▒▒██▒  ██▒▓██▒▀█▀ ██▒▒██    ▒ 
▓██ ░▄█ ▒▒██░  ██▒▒██░  ██▒▓██    ▓██░░ ▓██▄   
▒██▀▀█▄  ▒██   ██░▒██   ██░▒██    ▒██   ▒   ██▒
░██▓ ▒██▒░ ████▓▒░░ ████▓▒░▒██▒   ░██▒▒██████▒▒
░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░   ░  ░▒ ▒▓▒ ▒ ░
  ░▒ ░ ▒░  ░ ▒ ▒░   ░ ▒ ▒░ ░  ░      ░░ ░▒  ░ ░
  ░░   ░ ░ ░ ░ ▒  ░ ░ ░ ▒  ░      ░   ░  ░  ░  
   ░         ░ ░      ░ ░         ░         ░  
"""

# colors from the "settings.json"

with open("settings.json") as f: # we open the json and assign it a variable
	config = json.load(f) # we name the json.load so we can easily use it

# down there we get every possible color and style
PRIMARY_STG = config.get("primary-color").upper()
SECONDARY_STG = config.get("secondary-color").upper()
WHISPER_BG_STG = config.get("on-whisper-bg-color").upper()
WHISPER_FG_STG = config.get("on-whisper-fg-color").upper()
WHISPER_STYLE_STG = config.get("on-whisper-style").upper()
MENTION_BG_STG = config.get("on-mention-bg-color").upper()
MENTION_FG_STG = config.get("on-mention-fg-color").upper()
MENTION_STYLE_STG = config.get("on-mention-style").upper()


# and here we assign the colors from settings to a variable this way we can use it in text easily ;)
PRIMARY = getattr(Fore, PRIMARY_STG)
SECONDARY = getattr(Fore, SECONDARY_STG)
WHISPER_BG = getattr(Back, WHISPER_BG_STG)
WHISPER_FG = getattr(Fore, WHISPER_FG_STG)
WHISPER_STYLE = getattr(Style, WHISPER_STYLE_STG)
MENTION_BG = getattr(Back, MENTION_BG_STG)
MENTION_FG = getattr(Fore, MENTION_FG_STG)
MENTION_STYLE = getattr(Style, MENTION_STYLE_STG)

# here we assign Style.RESET_ALL a variable so we can easily use it, reset all resets the foreground color, background color and text style
SRESET = Style.RESET_ALL

# getting both tokens from the env
TOKEN = os.getenv('TOKEN')
REFRESH = os.getenv('REFRESH')

# defining our DogeClient class
class Client(DogeClient):
	def cls(self): #for clearing the console on any system
		os.system("cls" if os.name == "nt" else "clear")
	
	# asynchronous input! thanks to arthurdw (check the original repo: https://github.com/Arthurdw/EzChat)
	@staticmethod
	async def async_input(prompt: str = "") -> str:
		with ThreadPoolExecutor(1, "AsyncInput") as executor:
			return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)
	
	@event
	async def on_message(self, message: Message):
		try:
			if message.is_wisper == True:
				print(PRIMARY + f"@{message.author.username}: " + SRESET + WHISPER_FG + WHISPER_BG + WHISPER_STYLE + f"{message.content}" + SRESET + Style.BRIGHT + SECONDARY + "  (whisper)" + SRESET)
			else:
				if f"@{self.user.username}" in message.content:
					print(PRIMARY + f"@{message.author.username}: " + SRESET + MENTION_FG + MENTION_BG + MENTION_STYLE + f"{message.content}" + SRESET)
				else:
					print(PRIMARY + f"@{message.author.username}: " + SRESET + f"{message.content}")
		except Exception as e:
			print(e)

#as|y|lu|m

# clear the console when user gets ready and launch the firstRunMen
	@event
	async def on_ready(self):
		self.cls()
		global launchedtime
		launchedtime = datetime.datetime.now()
		await self.firstRunMenu()

# basically mainMenu but it has elapsed til start
	async def firstRunMenu(self):
		self.cls()
		elapsed = launchedtime - starttime
		elapsed = f"{elapsed.seconds}.{elapsed.microseconds}"
		print(PRIMARY + f"\n{DOGECLIASCII}\n" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Start-up finished in: " + SECONDARY + f"{elapsed} seconds" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Logged-in: " + SECONDARY + f"@{self.user}" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Creator: " + SECONDARY + "Asylum" + SRESET)
		print(PRIMARY + "\n\n[-] " + SRESET + "1: " + SECONDARY + "Commands" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "2: " + SECONDARY + "How-to" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "3: " + SECONDARY + "Initialize DogeHouse CLI" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "4: " + SECONDARY + "Settings" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "5: " + SECONDARY + "Credits" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "6: " + SECONDARY + "DogeHouse Profile" + SRESET)
		try: #here were putting this in a try except bc it wouldnt work if they pressed enter
			inputInteger = int(await self.async_input("\n\n" + PRIMARY + "[+] " + SRESET + "Choose your desired category..." + SRESET)) # A ;)
			if inputInteger == 1:
				await self.commandsMenu()
			elif inputInteger == 2:
				await self.howToMenu()
			elif inputInteger == 3:
				await self.initDogeCLIstart()
			elif inputInteger == 4:
				await self.settingsMenu()
			elif inputInteger == 5:
				await self.creditsMenu()
			elif inputInteger == 6:
				await self.profileMenu()
			else:
				await self.firstRunMenu()
		except:
			await self.firstRunMenu()


		
#|a|s|y|l|u|m
# the main menu with every category
	async def mainMenu(self):
		self.cls()
		print(PRIMARY + f"\n{DOGECLIASCII}\n" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Logged-in: " + SECONDARY + f"@{self.user}" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Creator: " + SECONDARY + "Asylum" + SRESET)
		print(PRIMARY + "\n\n[-] " + SRESET + "1: " + SECONDARY + "Commands" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "2: " + SECONDARY + "How-to" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "3: " + SECONDARY + "Initialize DogeHouse CLI" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "4: " + SECONDARY + "Settings" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "5: " + SECONDARY + "Credits" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "6: " + SECONDARY + "DogeHouse Profile" + SRESET)
		try: #here were putting this in a try except bc it wouldnt work if they pressed enter
			inputInteger = int(await self.async_input("\n\n" + PRIMARY + "[+] " + SRESET + "Choose your desired category..." + SRESET)) # A ;)
			if inputInteger == 1:
				await self.commandsMenu()
			elif inputInteger == 2:
				await self.howToMenu()
			elif inputInteger == 3:
				await self.initDogeCLIstart()
			elif inputInteger == 4:
				await self.settingsMenu()
			elif inputInteger == 5:
				await self.creditsMenu()
			elif inputInteger == 6:
				await self.profileMenu()
			else:
				await self.mainMenu()
		except:
			await self.mainMenu()
	
	async def chatRoom(self):
		self.cls()
		print(PRIMARY + "\n[-] " + SRESET + f"You have joined " + SECONDARY + f"{self.room.name}" + SRESET)
		inRoom = True
		while inRoom == True:
			inputStr = await self.async_input("\n")
			if inputStr.startswith("c/"):
				if inputStr.startswith("c/leave"):
					inRoom = False
					await self.initDogeCLIstart()
					await self.leave_room()
			else:
				await self.send(inputStr)
	
	async def commandsMenu(self):
		self.cls()
		print(SECONDARY + "[!] " + SRESET + "This category is WIP,\n you will be redirected back\n to the main menu in 5 seconds..." + SRESET) # Asylumhaha
		await asyncio.sleep(5)
		await self.mainMenu()
	
	async def howToMenu(self):
		self.cls()
		print(SECONDARY + "[!] " + SRESET + "This category is WIP,\n you will be redirected back\n to the main menu in 5 seconds..." + SRESET) #aysaylum
		await asyncio.sleep(5)
		await self.mainMenu()

	async def initDogeCLIstart(self):
		self.cls()
		try:
			print(PRIMARY + f"\n{ROOMSASCII}\n\n" + SRESET)
			roomNum = 0
			roomList = []
			for i in range(10):
				try:
					print(PRIMARY + f"\n[-] {i}: " + SRESET + f"Room Name:" + SECONDARY + f"{self.rooms[i].name}" + SRESET + f"• Description: " + SECONDARY + f"{self.rooms[i].description}" + SRESET + "• Member Count: " + SECONDARY + f"{self.rooms[i].count}" + SRESET)
					roomNum += 1
					roomList.append(self.rooms[i].id)
				except IndexError:
					break
			try: #here were putting this in a try except bc it wouldnt work if they pressed ente
				inputIntger = await self.async_input("\n\n" + PRIMARY + "[+] " + SRESET + "Choose the room you wanna join... (or if you don't see the room here, type the room ID)\nTo go back to the Main Menu, type " + Style.BRIGHT + "B" + SRESET)
				if inputIntger.lower() == 'b':
					await self.mainMenu()
				if len(inputIntger) == 1 or 2:
					try:
						roomID = roomList[int(inputIntger)]
						await self.join_room(roomID)
						await asyncio.sleep(0.5)
						await self.chatRoom()
					except Exception as e:
						print(SECONDARY + "\n[!] " + SRESET + f"Error: {e}")
						await asyncio.sleep(3)
						await self.initDogeCLIstart()
				else:
					try:
						await self.join_room(str(inputIntger))
						await asyncio.sleep(0.5)
						await self.chatRoom()
					except Exception as e:
						print(SECONDARY + "\n[!] " + SRESET + f"Error: {e}...")
						await asyncio.sleep(3)
						await self.initDogeCLIstart()
					
			except:
				await self.initDogeCLIstart()
		except Exception as e:
			print(e)
	
	
	
		

	async def settingsMenu(self):
		self.cls()
		print(SECONDARY + "[!] " + SRESET + "This category is WIP,\n you will be redirected back\n to the main menu in 5 seconds..." + SRESET) #aslm
		await asyncio.sleep(5)
		await self.mainMenu()
    
	async def creditsMenu(self):
		self.cls()
		print(PRIMARY + f"\n{CREDITSASCII}\n"+ SRESET)
		print(PRIMARY + "\n\n[-] " + SRESET + "Creator: " + SECONDARY + "Asylum" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Creator's Github: " + SECONDARY + "github.com/asxlvm" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Creator's Discord: " + SECONDARY + "Asylum#1759" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Creator's DogeHouse: " + SECONDARY + "@asylum" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Creator of DogeHouse.py lib: " + SECONDARY + "github.com/Arthurdw" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "CLI Github Repo: " + SECONDARY + "github.com/asxlvm/DogeCLI" + SRESET)
		try:
			goBackMain = await self.async_input("\n\n" + PRIMARY + "[+] " + SRESET + "Press anything to go back...") # A ;)
			if goBackMain:
				await self.mainMenu()
			else:
				await self.mainMenu()
		except:
			await self.mainMenu()


	
	async def profileMenu(self):
		self.cls()
		print(PRIMARY + f"\n{PROFILEASCII}\n"+ SRESET)
		print(PRIMARY + "\n\n[-] " + SRESET + "Username: " + SECONDARY + f"@{self.user.username}" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Display Name: " + SECONDARY + f"{self.user.displayname}" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "ID: " + SECONDARY + f"{self.user.id}" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Bio: " + SECONDARY + f"{self.user.bio}" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Followers: " + SECONDARY + f"{self.user.num_followers}" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Following: " + SECONDARY + f"{self.user.num_following}" + SRESET)
		print(PRIMARY + "\n[-] " + SRESET + "Avatar URL: " + SECONDARY + f"{self.user.avatar_url}" + SRESET)
		try:
			goBackMain = await self.async_input("\n\n" + PRIMARY + "[+] " + SRESET + "Press anything to go back...") # A ;)
			if goBackMain:
				await self.mainMenu()
			else:
				await self.mainMenu()
		except:
			await self.mainMenu()
		
Client(TOKEN, REFRESH, prefix="!", reconnect_voice=True).run()
