from discord.embeds import Embed
from discord.ext import tasks
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Cog
from discord.ext.commands import Context
from pymongo.errors import ConnectionFailure
from app.services.logger import  Logger
from app.modules.windows import Windows
from app.modules.permissions import is_guild_owner
from app.extension.database import DATABASES
from app.config import MONGODB_SERVER_IP
from app.config import MONGODB_SERVER_PORT


class RSS(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = Logger.generate_log()
        self.task = self.update_feed.start()
    
    @commands.command("subscribe")
    @commands.check(is_guild_owner())
    async def subscribe(self, ctx: Context):
        """
        Subscribe to a feed
        """
        db = DATABASES(host_name=str(MONGODB_SERVER_IP), host_port=int(MONGODB_SERVER_PORT))
        channel_ids = await db.get_all_channel("channel_id")
        if ctx.channel.id not in channel_ids:
            await db.add_channel(guild_id=ctx.guild.id, channel_id=ctx.channel.id)
            await ctx.send(f"{ctx.author.mention}, you are now subscribed to Windows Insider news")
        else:
            await ctx.send(f"{ctx.author.mention}, you are already subscribed to Windows Insider news")

    @commands.command("unsubscribe")
    @commands.check(is_guild_owner())
    async def unsubscribe(self, ctx: Context):
        """Unsubscribe from a feed"""
        db = DATABASES(host_name=str(MONGODB_SERVER_IP), host_port=int(MONGODB_SERVER_PORT))
        channel_ids = await db.get_all_channel("channel_id")
        if ctx.channel.id in channel_ids:
            await db.remove_channel(guild_id=ctx.guild.id, channel_id=ctx.channel.id)
            await ctx.send(f"{ctx.author.mention}, you are now unsubscribed from Windows Insider news")
        else:
            await ctx.send(f"{ctx.author.mention}, you are not subscribed to Windows Insider news")

    @tasks.loop(minutes=5)
    async def update_feed(self):
        """Update feed"""
        await self.bot.wait_until_ready()
        try:
            core = Windows(
                host_name=str(MONGODB_SERVER_IP), 
                host_port=int(MONGODB_SERVER_PORT)
            )
            result = await core.parseFeed()
        except ConnectionFailure:
            if self.task.cancel():
                await self.bot.close()

        if result["return"]:
            feeds: list = result["feeds"]
            ogp = core.get_opengraph(feeds)
            image = ogp["ogp"]["image"]
            embed = Embed(
                title=feeds[0]["title"], 
                url=feeds[0]["link"], 
                description=feeds[0]["description"],
            )
            embed.set_image(url=image)
            db = DATABASES(host_name=str(MONGODB_SERVER_IP), host_port=int(MONGODB_SERVER_PORT))
            channel_ids = await db.get_all_channel("channel_id")
            for channel_id in channel_ids:
                if not channel_id == None:
                    self.logger.debug(f"send {channel_id}")
                    await self.bot.get_channel(channel_id).send(
                        embed=embed
                    )


def setup(bot):
    bot.add_cog(RSS(bot))

