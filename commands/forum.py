import discord
from discord.ext import commands
from utils import info, data
import datetime
import json
import random

class Button(discord.ui.View):
    def __init__(self, bot: commands.Bot, thread: discord.Thread, message: discord.Message):
        super().__init__(timeout=None)
        self.bot = bot 
        self.thread = thread
        self.message = message  

    @discord.ui.button(label="Physics", style=discord.ButtonStyle.green, custom_id="physics", emoji="⚛️")
    async def role_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.thread.send(f"<@&{info.Physics}>")
        await self.message.edit(content=f"Thank you for your response {interaction.user.mention}.", view=None, embed=None, delete_after= 10)
        color = random.choice(info.colors)
        em= discord.Embed(title="Note for OP",
                          description="`+solved @user` to close the thread when your doubt is solved. Mention the user who helped you solve the doubt. This will be added to their stats.",
                          color=color)
        await self.thread.send(embed=em)

    @discord.ui.button(label="Chemistry", style=discord.ButtonStyle.green, custom_id="chemistry", emoji="🧪")
    async def role_two(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.thread.send(f"<@&{info.Chemistry}>")
        await self.message.edit(content=f"Thank you for your response {interaction.user.mention}.", view=None, embed=None, delete_after=10)
        color = random.choice(info.colors)
        em= discord.Embed(title="Note for OP",
                          description="`+solved @user` to close the thread when your doubt is solved. Mention the user who helped you solve the doubt. This will be added to their stats.",
                          color=color)
        await self.thread.send(embed=em)

    @discord.ui.button(label="Maths", style=discord.ButtonStyle.green, custom_id="maths", emoji="📏")
    async def role_three(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.thread.send(f"<@&{info.Maths}>")
        await self.message.edit(content=f"Thank you for your response {interaction.user.mention}.", view=None, embed=None, delete_after=10)
        color = random.choice(info.colors)
        em= discord.Embed(title="Note for OP",
                          description="`+solved @user` to close the thread when your doubt is solved. Mention the user who helped you solve the doubt. This will be added to their stats.",
                          color=color)
        await self.thread.send(embed=em)

    @discord.ui.button(label="Biology", style=discord.ButtonStyle.green, custom_id="biology", emoji="🦠")
    async def role_four(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.thread.send(f"<@&{info.Biology}>")
        await self.message.edit(content=f"Thank you for your response {interaction.user.mention}", view= None, embed=None, delete_after=10)
        color = random.choice(info.colors)
        em= discord.Embed(title="Note for OP",
                          description="`+solved @user` to close the thread when your doubt is solved. Mention the user who helped you solve the doubt. This will be added to their stats.",
                          color=color)
        await self.thread.send(embed=em)

class Forum(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.forum_channel_id = info.Forum_channel_ID

    # Event that will send the message
    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread):
        if thread.parent_id == self.forum_channel_id:
            owner = thread.owner_id
            color = random.choice(info.colors)
            em = discord.Embed(title= "Choose the Study Helper subject ping",
                               description="Choose the subject for the respective doubt :)",
                               color = color)            
            message = await thread.send(f"Hello <@{owner}>!", embed=em)
            button = Button(self.bot, thread, message)
            await message.edit(view=button)

    # Command for members to close the thread. Note: Everyone can close the thread. Admins can deduct their points.
    @commands.command(name="solved")
    @commands.cooldown(1, 120, commands.BucketType.user) # Cooldown set to 2 mins
    async def solve(self, ctx: commands.Context, user: discord.Member):
        forum_channel_id = info.Forum_channel_ID 
        if user.id == ctx.author.id:
            await ctx.send(":x: You cannot do that", delete_after=5)
        elif user.bot:
            await ctx.send(":x: You cannot do that.", delete_after=5)
        elif user:
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

    # Mod only command
    @commands.command(name="reopen")
    @commands.has_permissions(manage_threads=True)
    async def reopen(self, ctx: commands.Context):
        forum_channel_id = info.Forum_channel_ID  
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
                        await thread.edit(locked=False, archived=False, applied_tags=tags_to_add)
                        em = discord.Embed(title="Post unlocked and unarchived successfully!", color= 0x575287)
                        em.add_field(name="Unarchived by", value=f"{ctx.author.mention} ({ctx.author.id})")
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

async def setup(bot):
    await bot.add_cog(Forum(bot))