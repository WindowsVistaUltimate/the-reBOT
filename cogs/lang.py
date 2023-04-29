import discord
from discord.ext import commands
from botik import x
import sqlite3
from random import randint as random
conn = sqlite3.connect("./database/langs.db")
cur = conn.cursor()
def get_guild_lang(guildid: int) -> str:
    """fetches sqlite database to get language"""
    cur.execute("SELECT lang FROM langs WHERE guildid = ?", (guildid,))
    data = cur.fetchall()
    if data: return data[0][0]
    else: return "en"
class Language(commands.Cog):
    command = commands.hybrid_command
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    @command(description="Language options")
    async def lang(self, ctx: commands.Context):
        if ctx.author.guild_permissions.administrator:
            langbtns = discord.ui.View(timeout=None)
            langbtns.add_item(discord.ui.Button(label="English", custom_id="lang_en"))
            langbtns.add_item(discord.ui.Button(label="Русский", custom_id="lang_ru"))
            await ctx.send(embed=discord.Embed(title="Choose language:"), view = langbtns)
        else:
            await ctx.send(embed=discord.Embed(title=f"{x} Недостаточно прав!"))
    @commands.Cog.listener("on_interaction")
    async def on_lang(self, interaction: discord.Interaction):
        cur.execute("CREATE TABLE IF NOT EXISTS langs(guildid INTEGER, lang TEXT)")
        if interaction.type == discord.InteractionType.component:
            send = interaction.response.send_message
            try:
                option = str(interaction.data['custom_id'])
            except:
                pass
            else:
                if option == "lang_ru" or option == "lang_en":
                    lang = option.split("_")[1]
                    if interaction.user.guild_permissions.administrator:
                        cur.execute("SELECT guildid FROM langs WHERE guildid = ?", (interaction.guild.id,))
                        if cur.fetchall(): cur.execute("DELETE FROM langs WHERE guildid = ?", (interaction.guild.id,))
                        cur.execute("INSERT INTO langs(guildid, lang) VALUES(?,?)", (interaction.guild.id, lang))
                        conn.commit()
                        if lang == "ru":
                            await send(embed=discord.Embed(title="Язык успешно выбран!"), ephemeral=True)
                        if lang == "en":
                            await send(embed=discord.Embed(title="Language choosen successfully!"), ephemeral=True)
                    else:
                        await send(embed=discord.Embed(title="No"), ephemeral=True)
async def setup(bot):
    await bot.add_cog(Language(bot))
