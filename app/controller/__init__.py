import time

from typing import List, Optional
from app.services import WindowsInsider
from app.services.logger import Logger
from app.modules.errors import (
    DISCORD_COG_LOAD_FAILED,
    DISCORD_COG_RELOAD_FAILED
)
from app.config import (
    DISCORD_BOT_TOKEN, 
    DISCORD_BOT_VERSION,
    MONGODB_SERVER_IP,
    MONGODB_SERVER_PORT
)


class Controller:
    def __init__(self) -> None:
        self.log = Logger.generate_log()

        self.DISCORD_BOT_TOKEN = DISCORD_BOT_TOKEN
        self.DISCORD_BOT_VERSION = DISCORD_BOT_VERSION
        self.MONGODB_SERVER_IP = MONGODB_SERVER_IP
        self.MONGODB_SERVER_PORT = MONGODB_SERVER_PORT
        self.controller: Optional[WindowsInsider] = None
    
    async def on_ready(self):
        self.log.info("------------------------------------------------------------")
        self.log.info(f"[*] Logged is as [{self.controller.user.name}]")
        self.log.info(f"[*] CID: {str(self.controller.user.id)}")
        self.log.info(f"[*] Copyright (C) 2021 zeroday0619")
        self.log.info("------------------------------------------------------------")
        self.log.info(f"[*] Completed!")
        await self.controller.change_status.start()

    @Logger.set()
    def load_extensions(self, _cogs: List[str]):
        for extension in _cogs:
            try:
                self.controller.load_extension(extension)
            except Exception as ex:
                raise DISCORD_COG_LOAD_FAILED(extension=extension, msg=ex)

    @Logger.set()
    def reload_extensions(self, _cogs: List[str]):
        for extension in _cogs:
            try:
                self.controller.reload_extension(extension)
            except Exception as ex:
                raise DISCORD_COG_RELOAD_FAILED(extension=extension, msg=ex)

    def initialize(self):
        if not self.DISCORD_BOT_TOKEN:
            self.log.info(f"[*] Checking if Discord Bot token exists...")
            time.sleep(3)
            self.log.error("[*] Discord Bot Token is not found.")
            self.log.info(f"[*] Terminate startup process.")
            exit(1)
        else:
            self.log.info(f"[*] Checking if Discord Bot token exists... pass")
        if not self.MONGODB_SERVER_IP:
            self.log.info(f"[*] Checking if MongoDB server ip exists...")
            time.sleep(3)
            self.log.error("[*] MongoDB Server IP is not found.")
            self.log.info(f"[*] Terminate startup process.")
            exit(1)
        else:
            self.log.info(f"[*] Checking if MongoDB server  exists... pass")
        if not self.MONGODB_SERVER_PORT:
            self.log.info(f"[*] Checking if MongoDB Server port exists...")
            time.sleep(3)
            self.log.error("[*] MongoDB server port is not found.")
            self.log.info(f"[*] Terminate startup process.")
            exit(1)
        else:
            self.log.info(f"[*] Checking if MongoDB Server port exists... pass")
        
        self.log.info(f"[*] Initializing Discord Bot...")
        self.init()

    @Logger.set()
    def init(self):
        self.controller = WindowsInsider(
            discord_token=self.DISCORD_BOT_TOKEN,
            owner_id=541635951689072661,
            command_prefix="+",
            case_insensitive=True,
            description="Windows Insider news",
            message=["+help", "문의: zeroday0619#2080"],
            version="BETA 1.0.0"
        )