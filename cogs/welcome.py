import discord
from discord.ext import commands
from discord import app_commands, ui
import datetime

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = member.guild.get_channel(123456789012345678)
        if welcome_channel:
            WelcomeLayout = discord.ui.LayoutView()
            WelcomeContainer = discord.ui.Container(
                discord.ui.Section("## <:CraftAttackLogo:1447611436061819025> Craft Attack 13 Community Server\n"
                                   f"Willkommen auf unserem Server {member.mention}!\n\n",
                                   accessory=discord.ui.Thumbnail(media=f"{member.guild.icon}")),
                discord.ui.Separator(),
                discord.ui.TextDisplay(f"-# {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}"),
            )

            WelcomeLayout.add_item(WelcomeContainer)

            await welcome_channel.send(view=WelcomeLayout)

    @app_commands.command()
    async def welcome(self, interaction: discord.Interaction):
        WelcomeLayout = discord.ui.LayoutView()
        container = discord.ui.Container(
            discord.ui.Section("## <:CraftAttackLogo:1447611436061819025> Craft Attack 13 Community Server\n"
                               f"Willkommen auf unserem Server <@1178085568488415272>!\n\n",
                               accessory=discord.ui.Thumbnail(media=f"{interaction.guild.icon}")),
            discord.ui.Separator(),
            discord.ui.TextDisplay(f"-# {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}"),
        )

        WelcomeLayout.add_item(container)

        await interaction.channel.send(view=WelcomeLayout)
        await interaction.response.send_message("Container wurde erfolgreich gesendet!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))