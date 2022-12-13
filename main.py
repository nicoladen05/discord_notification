import discord
from pushbullet import Pushbullet
from dotenv import load_dotenv
from os import environ

user_list = [
    'blindniete#2156',
    'Gurkenglass#5992',
    'Netfelix#4473',
    'nicoladen#6604'
]

# Load dotenv
load_dotenv()

# Discord API credentials
DISCORD_BOT_TOKEN = environ["DISCORD_TOKEN"]

# Pushbullet API credentials
PUSHBULLET_API_KEY = environ["PUSHBULLET_TOKEN"]

# Create a Discord client
intents = discord.Intents().all()

#intents.members = True
#intents.presences = True

client = discord.Client(intents=intents)

# Create a Pushbullet client
pb = Pushbullet(PUSHBULLET_API_KEY)

@client.event
async def on_ready():
    # When the bot comes online, print a message
    print(f"Logged in as {client.user}")

@client.event
async def on_presence_update(before, after):
    #Check if the user is in user_list
    if str(before) in user_list:
        # If the user starts playing a game or comes online
        if (before.status != after.status):
            # Send a notification to the specified device
            # Test if the user has came online of offline
            if str(before.status) == 'offline':
                pb.push_note("Status update", f"{after} has come online.")
            elif str(after.status) == 'offline':
                pb.push_note("Status update", f"{after} is now offline.")
        
        elif (before.activity != after.activity):
            # Send a notification to the specified device
            if after.activity == None:
                pb.push_note("Game update", f"{after} has stopped playing {before.activity.name}.")
            elif before.activity == None and after.activity is not None:
                pb.push_note("Game update", f"{after} has started playing {after.activity.name}.")

@client.event
async def on_voice_state_update(member, before, after):
    # If the user was in a voice channel before the update
    if before.channel is not None and after.channel is None:
        pb.push_note("Voice update", f"{member} left {before.channel.name}")
    # If the user is in a voice channel after the update
    if before.channel is None and after.channel is not None:
        pb.push_note("Voice update", f"{member} joined {after.channel.name}")

        

client.run(DISCORD_BOT_TOKEN)