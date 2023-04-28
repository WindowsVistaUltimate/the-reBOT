import discord
from discord.ext import commands
from botik import x
import json
from random import randint as random
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
                        with open("./database/langs.json", "r", encoding="utf-8") as f:
                            await send("e", ephemeral=True)
                            db = json.loads(f.read())
                            db[str(interaction.guild.id)] = lang
                        with open("./database/langs.json", "w", encoding="utf-8") as f:
                            f.write(json.dumps(db))
                        if lang == "ru":
                            await send(embed=discord.Embed(title="Язык успешно выбран!"), ephemeral=True)
                        if lang == "en":
                            await send(embed=discord.Embed(title="Language choosen successfully!"), ephemeral=True)
                    else:
                        await send(embed=discord.Embed(title="No"), ephemeral=True)
async def setup(bot):
    await bot.add_cog(Language(bot))
