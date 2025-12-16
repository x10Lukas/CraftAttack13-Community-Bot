import discord
from discord import app_commands
from discord.ext import commands, tasks
import aiohttp
import datetime
from db.manager import Database
from io import BytesIO

DEFAULT_ICON_URL = "https://cdn.mcstatus.me/default.png"
STATUS_URL = "https://api.mcstatus.io/v2/status/java/"
ICON_URL = "https://api.mcstatus.io/v2/icon/"
WIDGET_URL = "https://api.mcstatus.io/v2/widget/java/"

async def fetch_json(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"Fehler bei Abruf {url}: {resp.status}")
            return await resp.json()

async def fetch_mcstatus_status(ip: str, port: int = 25565):
    try:
        return await fetch_json(f"{STATUS_URL}{ip}:{port}")
    except Exception:
        return {
            "players": {"online": 0, "max": 0},
            "version": {"name": "Unbekannt"},
            "online": False,
            "motd": {"clean": "Keine MOTD verfügbar"}
        }

async def fetch_mcstatus_icon(ip: str, port: int = 25565):
    url = f"{ICON_URL}{ip}:{port}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            return await resp.read()

async def fetch_mcstatus_widget_image(ip: str, port: int = 25565):
    url = f"{WIDGET_URL}{ip}:{port}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            return await resp.read()

class McStatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_status_loop.start()

    @tasks.loop(minutes=1)
    async def update_status_loop(self):
        db = await Database.connect()
        async with db.execute("SELECT ip, port, channel_id, message_id, display_name FROM status_messages") as cursor:
            entries = await cursor.fetchall()

        for ip, port, channel_id, message_id, name in entries:
            try:
                channel = self.bot.get_channel(channel_id)
                if not channel:
                    continue
                msg = await channel.fetch_message(message_id)

                status_data = await fetch_mcstatus_status(ip, port)
                icon_bytes = await fetch_mcstatus_icon(ip, port)
                widget_bytes = await fetch_mcstatus_widget_image(ip, port)

                motd = status_data.get("motd", {}).get("clean", "Keine MOTD verfügbar")
                players_online = status_data.get("players", {}).get("online", 0)
                players_max = status_data.get("players", {}).get("max", 0)
                version = status_data.get("version", {}).get("name", "Unbekannt")
                status_online = "Online" if status_data.get("online", False) else "Offline"

                icon_file = None
                if icon_bytes:
                    icon_file = discord.File(BytesIO(icon_bytes), filename="server_icon.png")
                    icon_url = "attachment://server_icon.png"
                else:
                    icon_url = DEFAULT_ICON_URL

                widget_file = None
                if widget_bytes:
                    widget_file = discord.File(BytesIO(widget_bytes), filename="widget.png")

                UpdateLayoutView = discord.ui.LayoutView()
                UpdateContainer = discord.ui.Container(
                    discord.ui.Section("## <:CraftAttackLogo:1447611436061819025> Craft Attack 13 Community Server\n"
                                       f"### {motd}\n",
                                       accessory=discord.ui.Thumbnail(icon_url)),
                    discord.ui.MediaGallery(
                        discord.MediaGalleryItem(media="attachment://widget.png"),
                    ),
                    discord.ui.Separator(),
                    discord.ui.TextDisplay(f"-# {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}")
                )

                UpdateLayoutView.add_item(UpdateContainer)

                files = []
                if icon_file:
                    files.append(icon_file)
                if widget_file:
                    files.append(widget_file)

                await msg.edit(view=UpdateLayoutView, attachments=files)

            except Exception as e:
                print(f"Update fehlgeschlagen für {ip}:{port}: {e}")

    @app_commands.command(name="addserver", description="Fügt einen Minecraft-Server zur Überwachung hinzu")
    async def addserver(self, interaction: discord.Interaction):
        modal = McStatusModal(self)
        await interaction.response.send_modal(modal)

    @app_commands.command(name="status", description="Zeigt den Status aller gespeicherten Server an")
    async def status(self, interaction: discord.Interaction ):
        db = await Database.connect()
        async with db.execute("SELECT ip, port, display_name FROM servers") as cursor:
            servers = await cursor.fetchall()
        if not servers:
            await interaction.response.send_message("❌ Keine Server in der Datenbank gespeichert.", ephemeral=True)
            return
        await interaction.response.defer(thinking=True)

        for ip, port, name in servers:
            try:
                status_data = await fetch_mcstatus_status(ip, port)
                icon_bytes = await fetch_mcstatus_icon(ip, port)
                widget_bytes = await fetch_mcstatus_widget_image(ip, port)

                motd = status_data.get("motd", {}).get("clean", "Keine MOTD verfügbar")
                players_online = status_data.get("players", {}).get("online", 0)
                players_max = status_data.get("players", {}).get("max", 0)
                version = status_data.get("version", {}).get("name_clean", "Unbekannt")
                status_online = "Online" if status_data.get("online", False) else "Offline"

                # Icon
                icon_file = None
                if icon_bytes:
                    icon_file = discord.File(BytesIO(icon_bytes), filename="server_icon.png")
                    icon_url = "attachment://server_icon.png"
                else:
                    icon_url = DEFAULT_ICON_URL

                # Widget
                widget_file = None
                if widget_bytes:
                    widget_file = discord.File(BytesIO(widget_bytes), filename="widget.png")

                StatusLayoutView = discord.ui.LayoutView()
                StatusContainer = discord.ui.Container(
                    discord.ui.Section("## <:CraftAttackLogo:1447611436061819025> Craft Attack 13 Community Server\n"
                                       f"### {motd}\n",
                                       accessory=discord.ui.Thumbnail(icon_url)),
                    discord.ui.MediaGallery(
                        discord.MediaGalleryItem(media="attachment://widget.png"),
                    ),
                    discord.ui.Separator(),
                    discord.ui.TextDisplay(f"-# {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}")
                )

                StatusLayoutView.add_item(StatusContainer)

                files = []
                if icon_file:
                    files.append(icon_file)
                if widget_file:
                    files.append(widget_file)

                msg = await interaction.channel.send(view=StatusLayoutView, files=files if files else None)
                await interaction.followup.send("Nachricht Erfolgreich gesendet!", ephemeral=True)

                await db.execute("""
                    INSERT OR REPLACE INTO status_messages (ip, port, channel_id, message_id, display_name)
                    VALUES (?, ?, ?, ?, ?)
                """, (ip, port, interaction.channel_id, msg.id, name))
                await db.commit()

            except Exception as e:
                print(f"Fehler beim Anzeigen von {name}: {e}")

class McStatusModal(discord.ui.Modal, title="Minecraft Server Status"):
    server_ip = discord.ui.TextInput(label="Server IP/Domain", placeholder="play.hypixel.net", required=True)
    port = discord.ui.TextInput(label="Port", placeholder="25565", required=True)
    display_name = discord.ui.TextInput(label="Display Name", placeholder="Vanilla Server", max_length=50, required=True)

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        ip = self.server_ip.value.strip()
        port = int(self.port.value.strip()) if self.port.value else 25565
        display = self.display_name.value.strip()
        try:
            db = await Database.connect()
            await db.execute(
                "INSERT OR REPLACE INTO servers (ip, port, display_name) VALUES (?, ?, ?)",
                (ip, port, display)
            )
            await db.commit()
            await interaction.followup.send(f"✅ Server **{display}** hinzugefügt!", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Fehler: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(McStatusCog(bot))