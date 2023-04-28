import discord
from discord.ext import commands
class Avatar(commands.Cog):
    command = commands.hybrid_command
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

# ------------------------- Эмодзи ---------------------------- #

    @command(aliases=["smile", "смайл", "эмодзи", "эмоция"], description="Показывает эмодзи")
    async def emoji(self, ctx: commands.Context, emoji: discord.Emoji):
        embed = discord.Embed(title=f"Эмодзи {emoji}:")
        embed.set_image(url=emoji.url)
        await ctx.send(embed=embed)

# ------------------------- Аватар ---------------------------- #

    @command(aliases=["аватар", "ава"], description="Показывает аватар пользователя (или ваш)")
    async def avatar(self, ctx: commands.Context, *,  user: discord.User=None):
        if not user: user = ctx.author
        embed = discord.Embed(title=f"Аватар {user}")
        if user.avatar: embed.set_image(url=user.avatar)
        else: embed.set_image(url=user.display_avatar)
        await ctx.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Avatar(bot))
