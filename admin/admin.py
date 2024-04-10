import discord
from discord.ext import commands
import json
import config
from utils import data, info
import datetime


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command()
    async def status(self, ctx: commands.Context, activity: str, *, status: str):
        if ctx.author.id == config.OWNER_ID:
            activity = activity.lower()
            if activity == "playing" or activity == "p":
                await ctx.bot.change_presence(activity=discord.Game(name=status))
            elif activity == "listening" or activity == "l":
                await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
            elif activity == "watching" or activity == "w":
                await ctx.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
            elif activity == "custom" or activity == "c":
                custom_activity = discord.CustomActivity(name=status)
                await ctx.bot.change_presence(activity=custom_activity)
            else:
                await ctx.send("Invalid activity type. Please choose one of 'playing', 'listening', 'watching', 'streaming', or 'custom'.")
                return

            await ctx.send(f"Status set to \n**Activity:** {activity} \n**Status:** '{status}'")
        else:
            return
      

    @commands.command(name="set_question", aliases=['sq'])
    @commands.has_guild_permissions(administrator=True)
    async def set_questions(self, ctx: commands.Context, target_user: str, amount: int):
            
        if amount < 0:
            await ctx.send("Amount must be a positive number.")
            return

        target_user_id = int(target_user.strip("<@!>"))

        target_user = self.bot.get_user(target_user_id)

        if not target_user:
            await ctx.send("Invalid user ID. Make sure to provide a valid user ID.")
            return

        await data.open_account(target_user)

        users = await data.get_lb_data()
        target_user_id = str(target_user.id)

        if target_user_id not in users:
            await ctx.send(f"{target_user.name} needs to open an account first.")
            return

        users[target_user_id]["Questions"] = amount

        with open("lb.json", "w") as f:
            json.dump(users, f)

        await ctx.send(f"The Questions for {target_user.name} has been set to {amount}.")

    @commands.command(name="fsolved")
    @commands.has_guild_permissions(manage_threads=True)
    async def fsolve(self, ctx: commands.Context, user: discord.Member = None):
        forum_channel_id = info.Forum_channel_ID        
        if user is None: 
            if ctx.channel.parent_id == info.Forum_channel_ID:
                channel = ctx.guild.get_channel(forum_channel_id)
                if channel:
                    all_tags = channel.available_tags
                    solved_tag = discord.utils.get(all_tags, name="Solved")
                    if solved_tag:
                        tags_to_add = [solved_tag]
                        thread_id = ctx.channel.id  
                        thread = discord.utils.get(channel.threads, id=thread_id)
                        if thread:
                            current_time = datetime.datetime.now()
                            unix_timestamp = int(current_time.timestamp())
                            await thread.edit(locked=True, archived=True, applied_tags=tags_to_add)
                            em = discord.Embed(title="Post locked and archived successfully!", color= 0x575287)
                            em.add_field(name="Archived by", value=f"{ctx.author.mention} ({ctx.author.id})")
                            em.add_field(name="Time", value=f"<t:{unix_timestamp}:R>")

                            await ctx.send(embed=em)
                        else:
                            await ctx.send("Thread not found.")
                    else:
                        await ctx.send("The 'Solved' tag was not found.")
                else:
                    await ctx.send("The forum channel is not found.")
            else:
                await ctx.send("The channel is not within the specified category.")

        elif user.id == ctx.author.id:
            await ctx.send(":x: You cannot do that", delete_after=5)
        elif user.bot:
            await ctx.send(":x: You cannot do that.", delete_after=5)

        elif user is not None:
            if ctx.channel.parent_id == info.Forum_channel_ID:
                channel = ctx.guild.get_channel(forum_channel_id)
                if channel:
                    all_tags = channel.available_tags
                    solved_tag = discord.utils.get(all_tags, name="Solved")
                    if solved_tag:
                        tags_to_add = [solved_tag]
                        thread_id = ctx.channel.id  
                        thread = discord.utils.get(channel.threads, id=thread_id)
                        if thread:
                            current_time = datetime.datetime.now()
                            unix_timestamp = int(current_time.timestamp())
                            await thread.edit(locked=True, archived=True, applied_tags=tags_to_add)
                            em = discord.Embed(title="Post locked and archived successfully!", color= 0x575287)
                            em.add_field(name="Archived by", value=f"{ctx.author.mention} ({ctx.author.id})")
                            em.add_field(name="Time", value=f"<t:{unix_timestamp}:R>")
                            em.add_field(name="Solved by", value=f"{user.mention} ({user.id})")
                            await data.open_account(user)
                            users = await data.get_lb_data()
                            await ctx.send(embed=em)

                            Questions = 1
                            users[str(user.id)]["Questions"] += Questions

                            with open("lb.json", "w") as f:
                                json.dump(users, f)
                        else:
                            await ctx.send("Thread not found.")
                    else:
                        await ctx.send("The 'Solved' tag was not found.")
                else:
                    await ctx.send("The forum channel is not found.")
            else:
                await ctx.send("The channel is not within the specified category.")

        else:
            await ctx.send("Error!")

async def setup(bot):
    await bot.add_cog(Admin(bot))