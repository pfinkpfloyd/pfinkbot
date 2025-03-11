from typing import Optional

from discord import Client, Intents, app_commands, Object


class PfinkBotClient(Client):
    """
    Specialized client that syncs commands with specified guilds (servers) manually to avoid waiting for the global commands to sync
    """
    def __init__(self, *, intents: Intents, guilds_to_sync: Optional[list[int]]):
        super().__init__(intents=intents)
        self.guilds_to_sync = [] if guilds_to_sync is None else guilds_to_sync
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        for guild in self.guilds_to_sync:
            guild_object = Object(guild)
            self.tree.copy_global_to(guild=guild_object)
            await self.tree.sync(guild=guild_object)
