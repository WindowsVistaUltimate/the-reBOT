import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import aiohttp
class Rank(commands.Cog):
    command = commands.hybrid_command
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @command(aliases=["ранг"], description="Ранк")
    async def rank(self, ctx: commands.Context, m: discord.User=None):
        if not m: m = ctx.author
        ram_avatar = BytesIO()
        ram_bg = BytesIO()
        bg = Image.open("./img/rank.png").convert("RGBA")
        font = ImageFont.truetype('./fonts/comfortaa.ttf', 30)
        bg2 = ImageDraw.Draw(bg)
        bg2.text((120,15), str(m), (255, 255, 255), font=font)
        overlay_avatar = m.avatar.with_size(128) if m.avatar else m.display_avatar
        await overlay_avatar.save(ram_avatar)
        avatar = Image.open(ram_avatar).convert("RGBA")
        avatar = avatar.resize((100,100), resample=Image.NEAREST)
        bg.paste(avatar, (10, 10), avatar)
        bg.save(ram_bg, format="PNG")
        ram_bg.seek(0)
        embed = discord.Embed()
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=discord.File(ram_bg, filename="image.png"), embed=embed)
async def setup(bot):
    await bot.add_cog(Rank(bot))
