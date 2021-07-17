import os
import typing

MONGODB_SERVER_IP: typing.Optional[str] = os.environ.get("MONGODB_SERVER_IP")
MONGODB_SERVER_PORT: typing.Optional[int] = os.environ.get("MONGODB_SERVER_PORT")
DISCORD_BOT_TOKEN: typing.Optional[str] = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_BOT_VERSION: typing.Optional[str] = os.environ.get("DISCORD_BOT_VERSION")