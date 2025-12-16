import discord
from discord.ext import commands
from discord import app_commands, ui
import asyncio

CATEGORY = "tickets"

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Create a Ticket")
    async def ticket(self, interaction: discord.Interaction):
        await interaction.channel.send(view=TicketContainer())
        await interaction.response.send_message("Container wurde Erfolgreich Gesendet!", ephemeral=True)

class TicketContainer(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        self.thumbnail = discord.ui.Thumbnail(media="https://images-ext-1.discordapp.net/external/_wfJkrSs2seuGlZH8bwPzjlNG9NqVF0RaPRIbn3Mh_U/https/message.style/cdn/images/ebd3cc9b347dc567bfda4bcb725d395337e80d24b41453bfbc8b39a6e07351fd.png?format=webp&quality=lossless")
        self.title = discord.ui.Section("# Ticket Support\n\n"
                                        "Brauchst du Hilfe bei etwas, oder möchtest einen Spieler Reporten der sich nicht an unsere Regeln hält! Egal ob Frage, Problem oder einfach nur Verwirrung – eröffne ein Ticket und wir helfen dir gerne weiter!", accessory=self.thumbnail)
        self.select = TicketSelectMenu()
        self.footer = discord.ui.TextDisplay("-# Dieses Ticket System dient zur schnellen und strukturierten Kommunikation.")

        self.container = discord.ui.Container(
            self.title,
            self.select,
            discord.ui.Separator(spacing=discord.SeparatorSpacing.large),
            self.footer
        )

        self.add_item(self.container)

class TicketSelectMenu(discord.ui.ActionRow):
    def __init__(self):
        super().__init__()

    options = [
        discord.SelectOption(label="General Support", emoji="📨", value="general_support"),
        discord.SelectOption(label="Player Report", emoji="⚠️", value="player_report"),
        discord.SelectOption(label="Team Bewerbung", emoji="📩", value="team_bewerbung"),
        discord.SelectOption(label="Premium Support", emoji="💎", value="premium_shop"),
        discord.SelectOption(label="Bug Report", emoji="🐛", value="bug_report"),
    ]

    @discord.ui.select(placeholder="Wähle eine Ticket Kategorie", min_values=1, max_values=1, options=options)
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        if select.values[0] == "general_support":
            await interaction.response.send_modal(GeneralSupportModal())
            await interaction.message.edit(view=TicketContainer())

        elif select.values[0] == "player_report":
            await interaction.response.send_modal(PlayerReportModal())
            await interaction.message.edit(view=TicketContainer())

        elif select.values[0] == "team_bewerbung":
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, read_message_history=True, send_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            }
            category = discord.utils.get(interaction.guild.categories, name=CATEGORY)
            channel = await interaction.guild.create_text_channel(name=f"{interaction.user.display_name}", overwrites=overwrites, category=category)
            embed = discord.Embed(title="Ticket Created",
                                  description="Support will be with you shortly.",
                                  color=discord.Color.green())
            await channel.send(embed=embed)
            await interaction.response.send_message(f"I've opened a ticket for you at {channel.mention}", ephemeral=True)
            await interaction.message.edit(view=TicketContainer())

        elif select.values[0] == "premium_shop":
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, read_message_history=True,
                                                              send_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True,
                                                                  read_message_history=True),
            }
            category = discord.utils.get(interaction.guild.categories, name=CATEGORY)
            channel = await interaction.guild.create_text_channel(name=f"{interaction.user.display_name}", overwrites=overwrites, category=category)
            embed = discord.Embed(title="Ticket Created",
                                  description="Support will be with you shortly.",
                                  color=discord.Color.green())
            await channel.send(embed=embed)
            await interaction.response.send_message(f"I've opened a ticket for you at {channel.mention}", ephemeral=True)
            await interaction.message.edit(view=TicketContainer())

        elif select.values[0] == "bug_report":
            await interaction.message.edit(view=TicketContainer())
            await interaction.response.send_modal(BugReportModal())

        else:
            await interaction.response.send_message("Ungültige Auswahl.", ephemeral=True)
            return

class GeneralSupportModal(ui.Modal, title="Allgemeiner Support"):
    reason = ui.TextInput(
        label="Beschreibe dein Anliegen",
        style=discord.TextStyle.paragraph,
        placeholder="Bitte gib eine genaue Beschreibung deines Problems an.",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, read_message_history=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        }

        category = discord.utils.get(interaction.guild.categories, name=CATEGORY)
        channel = await interaction.guild.create_text_channel(
            name=f"{interaction.user.display_name}",
            overwrites=overwrites,
            category=category
        )

        view = TicketInfoView(self.reason.value, interaction.user)
        await channel.send(view=view)
        await interaction.response.send_message(f"Dein Ticket wurde erfolgreich erstellt: {channel.mention}", ephemeral=True)

class PlayerReportModal(ui.Modal, title="Spieler Report"):
    reason = ui.TextInput(
        label="Beschreibe dein Anliegen",
        style=discord.TextStyle.paragraph,
        placeholder="Bitte gib eine genaue Beschreibung deines Problems an.",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, read_message_history=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        }

        category = discord.utils.get(interaction.guild.categories, name=CATEGORY)
        channel = await interaction.guild.create_text_channel(
            name=f"{interaction.user.display_name}",
            overwrites=overwrites,
            category=category
        )

        view = TicketInfoView(self.reason.value, interaction.user)
        await channel.send(view=view)
        await interaction.response.send_message(f"Dein Ticket wurde erfolgreich erstellt: {channel.mention}", ephemeral=True)

class BugReportModal(ui.Modal, title="Bug Report"):
    reason = ui.TextInput(
        label="Beschreibe dein Anliegen",
        style=discord.TextStyle.paragraph,
        placeholder="Bitte gib eine genaue Beschreibung deines Problems an.",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, read_message_history=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        }

        category = discord.utils.get(interaction.guild.categories, name=CATEGORY)
        channel = await interaction.guild.create_text_channel(
            name=f"{interaction.user.display_name}",
            overwrites=overwrites,
            category=category
        )

        view = TicketInfoView(self.reason.value, interaction.user)
        await channel.send(view=view)
        await interaction.response.send_message(f"Dein Ticket wurde erfolgreich erstellt: {channel.mention}", ephemeral=True)

class TicketInfoView(discord.ui.LayoutView):
    def __init__(self, reason: str, user: discord.Member):
        super().__init__()

        self.container = discord.ui.Container(
            discord.ui.Section(
                "## Ticket Support\n"
                f"{user.mention}, vielen Dank für das Erstellen eines Tickets.\n"
                "Unser Team wird dein Anliegen schnellstmöglich bearbeiten.",
                accessory=discord.ui.Thumbnail(media=user.display_avatar.url)
            ),
            discord.ui.Separator(),
            discord.ui.TextDisplay("### Dein Anliegen"),
            discord.ui.TextDisplay(f"```md\n{reason}\n```"),
            discord.ui.Separator(),
            discord.ui.TextDisplay(f"> Erstellt am <t:{int(discord.utils.utcnow().timestamp())}:F>."),
            Ticket_Button()
        )

        self.add_item(self.container)

class Ticket_Button(discord.ui.ActionRow):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="🔒 Schließen", style=discord.ButtonStyle.blurple, custom_id="close")
    async def close(self, interaction: discord.Interaction, button):
        embed = discord.Embed(title="Close Ticket",
                              description="Deleting Ticket in less than `4 Seconds`...\n\n"
                                          "_If not you can do it manually!_",
                              color=discord.Color.orange())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await asyncio.sleep(4)
        await interaction.channel.delete()

    @discord.ui.button(label="👤 User", style=discord.ButtonStyle.green, custom_id="add_user")
    async def user(self, interaction: discord.Interaction, button):
        await interaction.response.send_modal(UserMdodal())

    @discord.ui.button(label="📌 Rolle", style=discord.ButtonStyle.green, custom_id="add_role")
    async def role(self, interaction: discord.Interaction, button):
        await interaction.response.send_modal(RoleMdodal())

class UserMdodal(ui.Modal, title="Add User to Ticket"):
    user = ui.TextInput(label="User ID", placeholder="User ID", style=discord.TextStyle.short, custom_id="add_user")

    async def on_submit(self, interaction: discord.Interaction) -> None:
        user = interaction.guild.get_member(int(self.user.value))
        if user is None:
            return  await interaction.response.send_message("Invalid User ID, make sure the user is in this guild!")
        overwrite = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        await interaction.channel.set_permissions(user, overwrite=overwrite)
        await interaction.response.send_message(content=f"{user.mention} has been add to this ticket!", ephemeral=True)

class RoleMdodal(ui.Modal, title="Add Role to Ticket"):
    role = ui.TextInput(label="Role ID", placeholder="Role ID", style=discord.TextStyle.short, custom_id="add_role")

    async def on_submit(self, interaction: discord.Interaction) -> None:
        role = interaction.guild.get_role(int(self.role.value))
        if role is None:
            return await interaction.response.send_message("Invalid Role ID, make sure the role is in this guild!")
        overwrite = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        await interaction.channel.set_permissions(role, overwrite=overwrite)
        await interaction.response.send_message(content=f"{role.mention} has been add to this ticket!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ticket(bot))
    bot.add_view(TicketContainer())
    bot.add_view(UserMdodal())
    bot.add_view(RoleMdodal())
