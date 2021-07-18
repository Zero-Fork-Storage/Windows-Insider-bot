from discord.guild import Guild
from discord.channel import TextChannel
from app.modules.windows import Windows


class DATABASES:
    def __init__(self, host_name: str, host_port: int) -> None:
        self.host_name = host_name
        self.host_port = host_port
    
    async def add_channel(self, guild_id: Guild.id, channel_id: TextChannel.id):
        """add channel to the database"""
        client = await Windows(
            host_name=self.host_name, 
            host_port=self.host_port
        ).create_engine() 
        WIB_SERVER = client["WIB_SERVER"]
        channel = WIB_SERVER.channel
        server_info = {"guild_id": guild_id, "channel_id": channel_id}
        channel.insert_one(server_info)
        
    async def remove_channel(self, guild_id: Guild.id, channel_id: TextChannel.id):
        """remove channel from the database"""
        client = await Windows(
            host_name=self.host_name, 
            host_port=self.host_port
        ).create_engine() 
        WIB_SERVER = client["WIB_SERVER"]
        channel = WIB_SERVER.channel
        server_info = {"guild_id": guild_id, "channel_id": channel_id}
        channel.delete_one(server_info)

    async def get_all_channel(self, types: str) -> list:
        """get channels from the database
        
        :param types: channel type 'all', 'channel_id', 'guild_id'
        """
        client = await Windows(
            host_name=self.host_name,
            host_port=self.host_port
        ).create_engine()
        WIB_SERVER = client["WIB_SERVER"]
        channel = WIB_SERVER.channel
        if types == "all":
            return [i for i in channel.find()]
        if types == "channel_id":
            return [i.get("channel_id") for i in channel.find()]
        if types == "guild_id":
            return [i.get("guild_id") for i in channel.find()]
        raise ValueError("types must be 'all', 'channel_id', 'guild_id'")
