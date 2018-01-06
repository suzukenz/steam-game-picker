import asyncio
import discord


class SendMessageClient(discord.Client):
    """
    this client sends a text message only once to discord channel
    and logout immediately
    """
    def __init__(self, channel, message):
        super().__init__()
        self.channel = channel
        self.message = message

    async def on_ready(self):
        try:
            for chn in self.get_all_channels():
                if chn.type == discord.ChannelType.text and chn.name == self.channel:
                    await self.send_message(chn, self.message)
        finally:
            await self.logout()

    def run(self, token):
        super().run(token)
