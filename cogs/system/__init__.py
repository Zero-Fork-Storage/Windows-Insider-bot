from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Cog



class System(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if hasattr(ctx.command, 'on_error'):
            return
        if isinstance(error, commands.MissingRequiredArgument): 
            await ctx.send(f'Missing argument: {error}')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'Bad argument: {error}')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Check failed: {error}')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f'Missing permissions: {error}')
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'Bot missing permissions: {error}')
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f'Not owner: {error}')
        elif isinstance(error, commands.MissingRole):
            await ctx.send(f'Missing role: {error}')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(f'No private messages: {error}')
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f'Command error: {error}')


def setup(bot: Bot):
    bot.add_cog(System(bot))
