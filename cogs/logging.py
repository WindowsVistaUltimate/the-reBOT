from discord.ext import commands
import discord
import sqlite3
conn = sqlite3.connect("./database/logchannels.db")
cur = conn.cursor()
class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    @commands.hybrid_command(description="Отображает список нововведений")
    async def logging(self, ctx: commands.Context, channel: discord.TextChannel):
        cur.execute("CREATE TABLE IF NOT EXISTS logchannels(channel INTEGER, guild INTEGER)")
        cur.execute("SELECT guild FROM logchannels WHERE guild = ?", (ctx.guild.id,))
        if not cur.fetchall():
            cur.execute("INSERT INTO logchannels(channel, guild) VALUES (?, ?)", (channel.id, ctx.guild.id))
            await ctx.send(embed=discord.Embed(title="✅ Был успешно установлен канал для логов"))
        else:
            cur.execute("DELETE FROM logchannels WHERE guild = ?", (ctx.guild.id,))
            await ctx.send(embed=discord.Embed(title="✅ Был успешно удален канал для логов"))
        conn.commit()
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        try:
            cur.execute("SELECT channel FROM logchannels WHERE guild = ?", (before.guild.id,))
            channel = cur.fetchall()
            if channel: channel = channel[0][0]
            else: return
            embed = discord.Embed(title=f"Был изменен {before}")
            if before.display_name != after.display_name:
                embed.add_field(name="Старый ник:", value=before.display_name)
                embed.add_field(name="Новый ник:", value=after.display_name)
            elif len(before.roles) != len(after.roles):
                oldroles = set([a.mention for a in before.roles])
                newroles = set([a.mention for a in after.roles])
                if len(before.roles) < len(after.roles): embed.add_field(name="Добавленные роли:", value="\n".join(list(newroles - oldroles))[:1023])
                else: embed.add_field(name="Убранные роли:", value="\n".join(list(oldroles - newroles))[:1023])
            else: return
            embed.add_field(name="Кто:",value=after.mention)
            await before.guild.get_channel(channel).send(embed=embed)
        except Exception as e:
            await before.guild.get_channel(channel).send(e)
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content != after.content:
            cur.execute("SELECT channel FROM logchannels WHERE guild = ?", (before.guild.id,))
            channel = cur.fetchall()
            if channel: channel = channel[0][0]
            else: return
            embed=discord.Embed(title="Изменено сообщение")
            a = before.content.replace("\n", "\n- ")
            b = after.content.replace("\n", "\n+ ")
            embed.add_field(name="Старое сообщение:",value=f"```diff\n- {a}```")
            embed.add_field(name="Новое сообщение:",value=f"```diff\n+ {b}```")
            embed.add_field(name="Автор:",value=before.author.mention)
            view = discord.ui.View()
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="Ссылка на сообщение", url=before.jump_url))
            await before.guild.get_channel(channel).send(embed=embed, view=view)
    @commands.Cog.listener()
    async def on_channel_edit(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        cur.execute("SELECT channel FROM logchannels WHERE guild = ?", (before.guild.id,))
        channel = cur.fetchall()
        if channel: channel = channel[0][0]
        else: return
        embed=discord.Embed(title="Изменен канал")
        if before.name != after.name:
            embed.add_field(name="Старое название:",value=f"```diff\n- {before.name}```")
            embed.add_field(name="Новое название:",value=f"```diff\n+ {after.name}```")
        try: before.slowmode_delay
        except: ...
        else: 
            if before.slowmode_delay != after.slowmode_delay:
                embed.add_field(name="Старый кулдаун:",value=f"```diff\n- {int(before.slowmode_delay)}```")
                embed.add_field(name="Новый кулдаун:",value=f"```diff\n+ {int(after.slowmode_delay)}```")
        try: before.bitrate
        except: ...
        else: 
            if before.bitrate != after.bitrate:
                embed.add_field(name="Старый битрейт:",value=f"```diff\n- {int(before.bitrate)}```")
                embed.add_field(name="Новый битрейт:",value=f"```diff\n+ {int(after.bitrate)}```")
        if before.category != after.category:
            if before.category: embed.add_field(name="Старая категория:",value=f"```diff\n+ {before.category.name}```")
            if after.category: embed.add_field(name="Новая категория:",value=f"```diff\n+ {after.category.name}```")
        view = discord.ui.View()
        view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="Ссылка на сообщение", url=before.jump_url))
        await before.guild.get_channel(channel).send(embed=embed, view=view)
    @commands.Cog.listener()
    async def on_message_delete(self, msg: discord.Message):
        cur.execute("SELECT channel FROM logchannels WHERE guild = ?", (msg.guild.id,))
        channel = cur.fetchall()
        if channel: channel = channel[0][0]
        else: return
        embed=discord.Embed(title="Удалено сообщение")
        embed.add_field(name="Содержание:",value=msg.content)
        embed.add_field(name="Автор:",value=msg.author.mention)
        await msg.guild.get_channel(channel).send(embed=embed)
async def setup(bot):
    await bot.add_cog(Logging(bot))