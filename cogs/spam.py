from discord.ext import commands
import sqlite3, discord
from random import choice
from cogs.lang import get_guild_lang
conn = sqlite3.connect("./database/spams.db")
cur = conn.cursor()
spamguilds = set([])
class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    @commands.has_permissions(manage_guild=True)
    @commands.hybrid_command(aliases=["спам"], description="Spam")
    async def spam(self, ctx: commands.Context, *, spamtext: str="Spam"):
        if get_guild_lang(ctx.guild) == "ru":
            spamalready = "❌ Спам уже идет"
            spamstop = "✅ Спам остановлен"
            spamstart = "✅ Спам начат"
        else:
            spamalready = "❌ Spam started already"
            spamstop = "✅ Spam has been stopped"
            spamstart = "✅ Spam has been started"
        if (ctx.guild.id in spamguilds) and spamtext != "Spam": await ctx.send(spamalready); return
        elif ctx.guild.id in spamguilds:
            spamguilds.remove(ctx.guild.id)
            await ctx.send(spamstop)
            return
        await ctx.send(spamstart)
        cur.execute("CREATE TABLE IF NOT EXISTS spamentries(guildid INTEGER, content TEXT)")
        cur.execute("SELECT content FROM spamentries WHERE guildid = ?", (ctx.guild.id,))
        output = cur.fetchall()
        spamguilds.add(ctx.guild.id)
        webhook = None
        if ctx.me.guild_permissions.manage_webhooks: 
            webhooks = await ctx.channel.webhooks()
            if webhooks: webhook = webhooks[0]
            else: 
                try: webhook = await ctx.channel.create_webhook(name="Spam")
                except: webhook = ctx.channel
        else:
            webhook = ctx.channel
        while ctx.guild.id in spamguilds: 
            try: await webhook.send(f"{spamtext} {choice(output)[0] if output else ''} {' '.join([a.url for a in ctx.message.attachments])}"[:1999])
            except: ...
    @commands.has_permissions(manage_guild=True)
    @commands.hybrid_command(aliases=["спам_добавить"], description="Adds message to spam")
    async def spam_add(self, ctx: commands.Context, *, text):
        cur.execute("CREATE TABLE IF NOT EXISTS spamentries(guildid INTEGER, content TEXT)")
        cur.execute("CREATE TRIGGER IF NOT EXISTS maxrows BEFORE INSERT ON spamentries WHEN (SELECT COUNT(*) FROM spamentries) >= 100 BEGIN SELECT RAISE(FAIL, 'too many rows'); END;")
        try: cur.execute("INSERT INTO spamentries VALUES(?, ?)", (ctx.guild.id, text)); conn.commit()
        except: return
        if get_guild_lang(ctx.guild) == "ru":
            await ctx.send(embed=discord.Embed(title="Было успешно добавлено в спам!"))
        else:
            await ctx.send(embed=discord.Embed(title="Added to spam successfully!"))
async def setup(bot):
    await bot.add_cog(Spam(bot))