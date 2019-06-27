from discord.ext import commands
import aiohttp
import random
import discord

class Weeb_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.command(pass_context=True, no_pm=True)
    async def neko(self, ctx):
        """Nekos! \o/ Warning: Some lewd nekos exist :eyes:"""
        async with self.session.get("https://nekos.life/api/neko") as resp:
            nekos = await resp.json()

        embed = discord.Embed(colour=discord.Colour.purple())
        embed.set_image(url=nekos['neko'])
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def pat(self, ctx, member: discord.Member):
        """Pat your senpai/waifu!"""
        author = ctx.message.author.mention
        mention = member.mention

        pat = "**{0} pats {1}!**"

        choices = ['http://i.imgur.com/10VrpFZ.gif', 'http://i.imgur.com/x0u35IU.gif', 'http://i.imgur.com/0gTbTNR.gif', 'http://i.imgur.com/hlLCiAt.gif', 'http://i.imgur.com/sAANBDj.gif']

        image = random.choice(choices)

        embed = discord.Embed(description=pat.format(mention, author), colour=discord.Colour.purple())
        embed.set_image(url=image)

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def kiss(self, ctx, member: discord.Member):
      """Kiss your senpai/waifu!"""
      author = ctx.message.author.mention
      mention = member.mention

      kiss = "**{0} kisses {1}**"

      choices = ['http://i.imgur.com/0D0Mijk.gif', 'http://i.imgur.com/TNhivqs.gif', 'http://i.imgur.com/3wv088f.gif', 'http://i.imgur.com/7mkRzr1.gif', 'http://i.imgur.com/8fEyFHe.gif']

      image = random.choice(choices)

      embed = discord.Embed(description=kiss.format(author, mention), colour=discord.Colour.blue())
      embed.set_image(url=image)

      await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def hug(self, ctx, member: discord.Member):
       """Hug your senpai/waifu!"""
       author = ctx.message.author.mention
       mention = member.mention

       hug = "**{0} hugs {1}**"

       choices = ['http://i.imgur.com/sW3RvRN.gif', 'http://i.imgur.com/gdE2w1x.gif', 'http://i.imgur.com/zpbtWVE.gif', 'http://i.imgur.com/ZQivdm1.gif', 'http://i.imgur.com/MWZUMNX.gif']

       image = random.choice(choices)

       embed = discord.Embed(description=hug.format(author, mention), colour=discord.Colour.blue())
       embed.set_image(url=image)

       await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Weeb_Commands(bot))
