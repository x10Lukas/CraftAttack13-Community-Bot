import discord
from dotenv import load_dotenv
import os
import ezcord
from db.manager import Database

class CraftAttackBot(ezcord.Bot):
    def __init__(self):
        load_dotenv()

        intents = discord.Intents.default()

        super().__init__(intents=intents, token=os.getenv("TOKEN"))

    async def on_ready(self):
        print(f"{self.user} ist ready!")
        await self.tree.sync()
        await Database.init_db()

if __name__ == "__main__":
    bot = CraftAttackBot()
    bot.load_cogs()
    bot.run()