from discord.ext import commands
from discord.ext.commands import Context

def is_guild_owner():
    def predicate(ctx: Context):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)


__all__ = [
    is_guild_owner
]