from app.controller import Controller
from app.services import WindowsInsider


class DiscordClient(Controller):
    def __init__(self):
        super(DiscordClient, self).__init__()
        self.event(self.on_ready)

    def event(self, coro):
        self.initialize()
        self.controller.event(coro)
    
    def _run(self):
        self.controller.lanuch()


class WIB(DiscordClient):
    def __init__(self):
        super(WIB, self).__init__()

    def run(self):
        self._run()
