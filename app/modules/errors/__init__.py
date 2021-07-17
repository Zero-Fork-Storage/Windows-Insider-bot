class DISCORD_COG_LOAD_FAILED(Exception):
    def __init__(self, extension, msg):
        self.extension = extension
        self.msg = msg

    def __str__(self):
        return f"Failed to load extension {self.extension}: {self.msg}"


class DISCORD_COG_RELOAD_FAILED(Exception):
    def __init__(self, extension, msg):
        self.extension = extension
        self.msg = msg

    def __str__(self):
        return f"Failed to reload extension {self.extension}: {self.msg}"