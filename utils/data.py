import discord
from discord.ext import commands
import json

class Data(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

async def open_account(user: discord.User):
    users = await get_lb_data()

    user_id = str(user.id)

    if user_id in users:
        return False
    else:
        users[user_id] = {}
        users[user_id]["Questions"] = 0 

    with open("lb.json", "w") as f:
        json.dump(users, f, indent= 2)

    return True

async def get_lb_data():
        with open("lb.json", "r") as f:
            users = json.load(f)

        return users  

async def setup(bot):
    await bot.add_cog(Data(bot))