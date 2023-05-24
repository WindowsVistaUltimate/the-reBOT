import discord
from discord.ext import commands
from cogs.lang import get_guild_lang
class Avatar(commands.Cog):
    command = commands.hybrid_command
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

# ------------------------- Эмодзи ---------------------------- #

    @command(aliases=["smile", "смайл", "эмодзи", "эмоция"], description="Показывает эмодзи")
    async def emoji(self, ctx: commands.Context, emoji: discord.Emoji):
        if get_guild_lang(ctx.guild) == "ru": emoji = "Эмодзи"
        else: emoji = "Emoji"
        embed = discord.Embed(title=f"{emoji} {emoji}:")
        embed.set_image(url=emoji.url)
        await ctx.send(embed=embed)

# ------------------------- Аватар ---------------------------- #

    @command(aliases=["аватар", "ава"], description="Показывает аватар пользователя (или ваш)")
    async def avatar(self, ctx: commands.Context, *,  user: discord.User=None):
        if get_guild_lang(ctx.guild) == "ru": avatar = "Аватар"
        else: avatar = "Avatar"
        if not user: user = ctx.author
        embed = discord.Embed(title=f"{avatar} {user}")
        if user.avatar: embed.set_image(url=user.avatar)
        else: embed.set_image(url=user.display_avatar)
        await ctx.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Avatar(bot))
