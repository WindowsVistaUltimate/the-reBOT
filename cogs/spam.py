from discord.ext import commands
import sqlite3, discord
from random import choice
from botik import iscreator
conn = sqlite3.connect("./database/spams.db")
cur = conn.cursor()
spamguilds = set([])
class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    @commands.has_permissions(manage_guild=True)
    @commands.hybrid_command(aliases=["spam"], description="Спам")
    async def спам(self, ctx: commands.Context, *, spamtext: str="Спам"):
        try:
            if (ctx.guild.id in spamguilds) and spamtext != "Спам": await ctx.send("❌ Спам уже идет"); return
            elif ctx.guild.id in spamguilds:
                spamguilds.remove(ctx.guild.id)
                await ctx.send("✅ Спам остановлен")
                return
            await ctx.send("✅ Спам начат")
            cur.execute("CREATE TABLE IF NOT EXISTS spamentries(guildid INTEGER, content TEXT)")
            cur.execute("SELECT content FROM spamentries WHERE guildid = ?", (ctx.guild.id,))
            output = cur.fetchall()
            spamguilds.add(ctx.guild.id)
            webhook = None
            if ctx.me.guild_permissions.manage_webhooks: 
                webhooks = await ctx.channel.webhooks()
                if webhooks: webhook = webhooks[0]
                else: webhook = await ctx.channel.create_webhook(name="Спам")
            else:
                webhook = ctx.channel
            while ctx.guild.id in spamguilds: 
                if type(webhook) == discord.Webhook:
                    try: await webhook.send(f"{spamtext} {choice(output)[0] if output else ''} {' '.join([a.url for a in ctx.message.attachments])}"[:1999], username="Спам")
                    except: ...
                else:
                    try: await webhook.send(f"{spamtext} {choice(output)[0] if output else ''} {' '.join([a.url for a in ctx.message.attachments])}"[:1999])
                    except: ...
        except Exception as e:
            await ctx.send(e)
    @commands.has_permissions(manage_guild=True)
    @commands.hybrid_command(aliases=["spam_add"], description="Добавляет сообщение в спам")
    async def спам_добавить(self, ctx: commands.Context, *, text):
        cur.execute("CREATE TABLE IF NOT EXISTS spamentries(guildid INTEGER, content TEXT)")
        cur.execute("CREATE TRIGGER IF NOT EXISTS maxrows BEFORE INSERT ON spamentries WHEN (SELECT COUNT(*) FROM spamentries) >= 100 BEGIN SELECT RAISE(FAIL, 'too many rows'); END;")
        try: cur.execute("INSERT INTO spamentries VALUES(?, ?)", (ctx.guild.id, text)); conn.commit()
        except: return
        await ctx.send(embed=discord.Embed(title="Было успешно добавлено в спам!"))
async def setup(bot):
    await bot.add_cog(Spam(bot))