from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.errors import CheckFailure
from app.services.logger import Logger


logger = Logger.generate_log()

def is_guild_owner():
    def predicate(ctx: Context):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    try:
        return commands.check(predicate)
    except CheckFailure as e:
        logger.error(f"[*] {e}")



__all__ = [
    is_guild_owner
]