import discord
from typing import List
from typing import Optional
from itertools import cycle
from discord.ext import tasks
from discord.ext.commands import Bot
from discord.ext.commands import HelpCommand


class WindowsInsider(Bot):
    """Windows Insider Core System"""
    def __init__(
        self, 
        discord_token: str, 
        owner_id: Optional[int] = None,
        command_prefix: Optional[str] = None,
        case_insensitive: bool = True,
        description: Optional[str] = None,
        message: Optional[List[str]] = None,
        version: Optional[str] = None
    ) -> None:
        """Initialize Windows Insider Bot
        
        :param discord_token: Discord BOT Token
        :param owner_id: Discord BOT Owner ID
        :param command_prefix: Discord BOT Command Prefix
        :param case_insensitive: Discord BOT Case Insensitive
        :param description: Discord BOT Description
        :param message: Discord BOT status Message
        :param version: Discord BOT Version
        """

        self.discord_token = discord_token
        self.owner_id = owner_id
        self.command_prefix = command_prefix
        self.case_insensitive = case_insensitive
        self.description = description
        self.message = message
        self.version = version

        super(WindowsInsider, self).__init__(
            command_prefix=self.command_prefix,
            case_insensitive=self.case_insensitive,
            description=self.description,
        )
    
    @tasks.loop(seconds=10)
    async def change_status(self) -> None:
        """Change BOT Status"""
        await self.change_presence(
            status=discord.Status.online, 
            activity=discord.Game(next(cycle(self.message)))
        )
        
    
    def lanuch(self) -> None:
        """Launch Windows Insider BOT"""
        self.run(self.discord_token)

        