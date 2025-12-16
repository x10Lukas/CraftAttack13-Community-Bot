import discord
from discord.ext import commands
from discord import app_commands

class RegelnCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="regeln", description="Zeigt die Serverregeln an")
    async def regeln(self, interaction: discord.Interaction):
        await interaction.channel.send(view=RegelnContainer())
        await interaction.response.send_message("Container wurde Erfolgreich Gesendet!", ephemeral=True)

class RegelnContainer(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        self.thumbnail = discord.ui.Thumbnail(media="https://images-ext-1.discordapp.net/external/_wfJkrSs2seuGlZH8bwPzjlNG9NqVF0RaPRIbn3Mh_U/https/message.style/cdn/images/ebd3cc9b347dc567bfda4bcb725d395337e80d24b41453bfbc8b39a6e07351fd.png?format=webp&quality=lossless")
        self.title = discord.ui.Section("## <:CraftAttackLogo:1447611436061819025> Craft Attack 13 Community Server\n"
                                        "## REGELWERK\n"
                                        "Hier findest du die Regeln des Craft Attack 13 Community Servers", accessory=self.thumbnail)
        self.regel1 = discord.ui.TextDisplay("### Giering\n"
                                             "Verboten ist:\n"
                                             "- Umgehen von Claimregeln um Bauwerke anderer zu zerstören\n"
                                             "- Lag bzw. Dupemaschinen welche die Leistung des Servers oder anderer Spieler beabsichtigt beeinflussen.\n"
                                             "- Wasser oder Lavabauten die nur zum nerven und beeinflussen der Optik anderer Spieler gebaut werden.\n"
                                             "- Explosionen auf oder an fremden Grundstücken um die Schutzmechaniken zu umgehen.\n"
                                             "- Entfernen von fremden Entities (Tiere, Monster, Armorstand etc.)\n"
                                             "- Das Verunstalten der Landschaft und Umgebung auf allen Servern Verhalten/Beleidigung/Skins.\n"
                                             "- TPA Fallen in jeglicher Form\n"
                                             "- Umgehen der PvP-Regeln durch Explosionen, Fallen oder jegliche sonstige Art\n"
                                             "- Beabsichtiges klauen von Fremdem Eigentum auf anderen Grundstücken (Itemdrops etc.)")
        self.regel2 = discord.ui.TextDisplay("### Umgang/Beleidigung/Skins/Namen\n"
                                             "Verboten ist:\n"
                                             "- Beleidigungen andere Spieler in jeglicher Form\n"
                                             "- Respektloses Verhalten gegenüber Mitspielern\n"
                                             "- Trolling in ernsten Situationen\n"
                                             "- Anstößige- / Sexualisierte- / Beleidigende- / nicht angebrachte Skins und Nicknamen\n"
                                             "- Missachten von Teamanweisungen\n"
                                             "- Politische Unterhaltungen und Statements im öffentlichen Chat und VoiceChat.\n"
                                             "- Caps sowie Spam.\n"
                                             "- Jegliche Art von Werbung die nicht mit craftattack.me zu tun hat\n"
                                             "- Sexuelle, Extremistische, Religionfeindliche und nicht jugendgerechte Ausdrucksweise.\n"
                                             "- Provozieren.\n"
                                             "- Drohen anderer Spieler.\n"
                                             "- Echtgeldhandel mit anderen Spielern.")
        self.regel3 = discord.ui.TextDisplay("### Client Modifikationen\n"
                                             "Verboten ist:\n"
                                             "- Hack- / Cheatclients\n"
                                             "- X-Ray (Ressourcepacks gehören auch dazu)\n"
                                             "- Worlddownloader\n"
                                             "- Anti AFK Modifikationen\n"
                                             "- Andere Modifikationen die dir gegenüber anderen Spielern einen Vorteil bringen könnten.")
        self.regel4 = discord.ui.TextDisplay("### Umgehen von Strafen\n"
                                             "- Das umgehen von Strafen durch Zweit/- oder Drittaccounts ist verboten.")
        self.regel5 = discord.ui.TextDisplay("### Generell gilt: Unwissenheit schützt vor Strafe nicht.\n"
                                             "**Anweisungen von Teammitgliedern ist folge zu leisten auch wenn eine das hier nicht gelistet ist.**")
        self.footer = discord.ui.TextDisplay("-# Änderungen Vorbehalten ")

        self.container = discord.ui.Container(
            self.title,
            discord.ui.Separator(spacing=discord.SeparatorSpacing.large),
            self.regel1,
            discord.ui.Separator(),
            self.regel2,
            discord.ui.Separator(),
            self.regel3,
            discord.ui.Separator(),
            self.regel4,
            discord.ui.Separator(),
            self.regel5,
            discord.ui.Separator(),
            self.footer
        )

        self.add_item(self.container)

async def setup(bot):
    await bot.add_cog(RegelnCog(bot))
    bot.add_view(RegelnContainer())