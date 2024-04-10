import discord
from discord.ext import commands
from utils import data


class lb(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="leaderboard", aliases=['lb'])
    async def leaderboard(self, ctx: commands.Context):
        users = await data.get_lb_data()
        leader_board = {}

        for member in ctx.guild.members:
            user_id = str(member.id)
            if user_id in users:
                total_questions = users[user_id].get("Questions", 0)
                leader_board[total_questions] = user_id

        total = sorted(leader_board.keys(), reverse=True)

        em = discord.Embed(title=f"Top 5 Users with most amount of Doubts solved in {ctx.guild.name}", description="This is decided on the basis of `+solved` command", color=discord.Color(0xfa43ee))
        index = 1
        for questions in total:
            user_id = leader_board[questions]
            member = ctx.guild.get_member(int(user_id))
            name = member.name if member else "Unknown User"
            em.add_field(name=f"{index}. {name}", value=f"Questions: {questions}", inline=False)
            if index == 5:
                break
            else:
                index += 1

        user_questions = users.get(str(ctx.author.id), {}).get("Questions", 0)
        if user_questions not in total:  
            total.append(user_questions)
            total.sort(reverse=True)
        user_rank = total.index(user_questions) + 1

        em.set_footer(text=f"Your Rank: #{user_rank}")

        await ctx.send(embed=em)

    @commands.command(name="stats")
    async def stats(sel, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member= ctx.author
        try:
            await data.open_account(member)
            users = await data.get_lb_data()
            Questions = users[str(member.id)]["Questions"]

            em = discord.Embed(title=f"{member.name}'s stats", color=0xeea990)
            em.set_thumbnail(url=member.display_avatar.url)
            em.add_field(name="Questions", value=f"{Questions}")
            await ctx.send(embed=em)
            
        except commands.BadArgument:
            await ctx.send("Invalid user provided.")

async def setup(bot):
    await bot.add_cog(lb(bot))
    