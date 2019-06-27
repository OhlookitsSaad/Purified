import time
import aiohttp
import discord
import asyncio

from asyncio.subprocess import PIPE
from discord.ext import commands
from io import BytesIO
from utils import repo, default, http, dataIO


class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self._last_result = None

    @commands.command()
    async def dev(self, ctx):
        """ Checks if you're a developer of Purified """
        if ctx.author.id in self.config.owners:
            return await ctx.send(f"Yes, this is {ctx.author.name}, my developer.")

    @commands.command()
    @commands.check(repo.is_owner)
    async def reload(self, ctx, name: str):
        """ Reloads a cog """
        try:
            self.bot.unload_extension(f"cogs.{name}")
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```\n{e}```")
        await ctx.send(f"✅ Successfully reloaded **{name}.py**")

    @commands.command()
    @commands.check(repo.is_owner)
    async def die(self, ctx):
        """ Kills the bot """
        await ctx.send('✅ Shutting down!')
        time.sleep(1)
        await self.bot.logout()

    @commands.command()
    @commands.check(repo.is_owner)
    async def load(self, ctx, name: str):
        """ Reloads a cog """
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```diff\n- {e}```")
        await ctx.send(f"✅ Successfully loaded **{name}.py**!")

    @commands.command()
    @commands.check(repo.is_owner)
    async def unload(self, ctx, name: str):
        """ Unloads a cog """
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```diff\n- {e}```")
        await ctx.send(f"✅ Successfully unloaded **{name}.py**!")

    @commands.group()
    @commands.check(repo.is_owner)
    async def set(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @set.command(name="playing")
    @commands.check(repo.is_owner)
    async def set_playing(self, ctx, *, playing: str):
        """ Change the bot's playing status """
        try:
            await self.bot.change_presence(
                activity=discord.Game(type=0, name=playing),
                status=discord.Status.online
            )
            dataIO.change_value("config.json", "playing", playing)
            await ctx.send(f"✅ Successfully changed playing status to **{playing}**")
        except discord.InvalidArgument as err:
            await ctx.send(err)
        except Exception as e:
            await ctx.send(e)

    @set.command(name="username")
    @commands.check(repo.is_owner)
    async def set_username(self, ctx, *, name: str):
        """ Change the bot's username """
        try:
            await self.bot.user.edit(username=name)
            await ctx.send(f"✅ Successfully changed my name to **{name}**")
        except discord.HTTPException as err:
            await ctx.send(err)

    @set.command(name="nickname")
    @commands.check(repo.is_owner)
    async def set_nickname(self, ctx, *, name: str = None):
        """ Change the bot's nickname in a server """
        try:
            await ctx.guild.me.edit(nick=name)
            if name:
                await ctx.send(f"✅ Successfully changed my nickname to **{name}**")
            else:
                await ctx.send("✅ Successfully removed my nickname")
        except Exception as err:
            await ctx.send(err)

    @set.command(name="avatar")
    @commands.check(repo.is_owner)
    async def set_avatar(self, ctx, url: str = None):
        """ Change the bot's avatar """
        if url is None and len(ctx.message.attachments) == 1:
            url = ctx.message.attachments[0].url
        else:
            url = url.strip('<>') if url else None

        try:
            bio = await http.get(url, res_method="read")
            await self.bot.user.edit(avatar=bio)
            await ctx.send(f"✅ Successfully changed the avatar, my current avatar is:\n{url}")
        except aiohttp.InvalidURL:
            await ctx.send("❌ The URL you provided is invalid!")
        except discord.InvalidArgument:
            await ctx.send("❌ The URL does not contain a useable image!")
        except discord.HTTPException as err:
            await ctx.send(err)
        except TypeError:
            await ctx.send("❌ You need to either provide an image URL or upload one with the command.")

    @commands.command(aliases=['exec'])
    @commands.check(repo.is_owner)
    async def execute(self, ctx, *, text: str):
        """ Executes a command in the Terminal """
        message = await ctx.send(f"Executing the command, please wait.")
        proc = await asyncio.create_subprocess_shell(text, stdin=None, stderr=PIPE, stdout=PIPE)
        out = (await proc.stdout.read()).decode('utf-8').strip()
        err = (await proc.stderr.read()).decode('utf-8').strip()

        if not out and not err:
            await message.delete()
            return await ctx.message.add_reaction('👌')

        content = ""

        if err:
            content += f"Error:\r\n{err}\r\n{'-' * 30}\r\n"
        if out:
            content += out

        if len(content) > 1500:
            try:
                data = BytesIO(content.encode('utf-8'))
                await message.delete()
                await ctx.send(content=f"⚠️ The result was a bit too long, so here is a text file instead.",
                               file=discord.File(data, filename=default.timetext(f'Result')))
            except asyncio.TimeoutError as e:
                await message.delete()
                return await ctx.send(e)
        else:
            await message.edit(content=f"```fix\n{content}\n```")


def setup(bot):
    bot.add_cog(Developer(bot))
