import discord
from discord.ext import commands
import config
import time

intents= discord.Intents.all()
bot = commands.Bot(command_prefix=['+','k!'], intents=intents, help_command=None, strip_after_prefix= True)


@bot.event
async def on_ready():
    custom_activity = discord.CustomActivity(name="Waking up ⛔")
    await bot.change_presence(status = discord.Status.do_not_disturb ,activity=custom_activity)
    print('Bot is ready.')

    
    await bot.load_extension("admin.admin")
    await bot.load_extension("admin.error")
    await bot.load_extension("commands.forum")
    await bot.load_extension("commands.lb")
    

    print("All cogs loaded")
    await bot.change_presence(activity=discord.Game(name="Hello World!"), status=discord.Status.online)
    print("Bot is Online")

@bot.command()
async def ping(ctx):
    start_time = time.time()
    message = await ctx.send("Pinging...")
    end_time = time.time()

    latency = round((end_time - start_time) * 1000)  
    api_latency = round(bot.latency * 1000)  

    await message.edit(content=f"Pong! Latency: **{latency}ms** | API Latency: **{api_latency}ms**")

bot.run(config.BOT_TOKEN)