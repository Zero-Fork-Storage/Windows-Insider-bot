from discord.embeds import Embed
from discord.ext import tasks
from discord.ext.commands import Bot
from discord.ext.commands import Cog
from app.config import MONGODB_SERVER_IP
from app.config import MONGODB_SERVER_PORT
from app.modules.windows import InsiderFeed

class RSS(Cog):
    def __init__(self, bot: Bot):
        self.rss_channel = 730764715936055309
        self.bot = bot
        self.update_feed.start()
    
    @tasks.loop(seconds=10)
    async def update_feed(self):
        """Update feed"""
        await self.bot.wait_until_ready()
        core = InsiderFeed(
            host_name=str(MONGODB_SERVER_IP), 
            host_port=int(MONGODB_SERVER_PORT)
        )
        result = await core.parseFeed()
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

            await self.bot.get_channel(self.rss_channel).send(
                embed=embed
            )


def setup(bot):
    bot.add_cog(RSS(bot))

