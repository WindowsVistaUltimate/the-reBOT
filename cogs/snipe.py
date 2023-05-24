import discord
from discord.ext import commands
import time
from discord import ButtonStyle, app_commands
import sqlite3
from ast import literal_eval as eval_
from botik import chk, iscreator, x
from cogs.lang import get_guild_lang
from typing import Union, Callable
command = commands.hybrid_command
conn = sqlite3.connect("./database/deleted_messages.db")
cur = conn.cursor()
async def showpage(member: Union[discord.Member, discord.User], ctx: Union[discord.Interaction, commands.Context], page: int, send: Callable, edit: Callable=None) -> None:
    """we don't need to type that twice"""
    if not edit: edit = send; isinteraction = False
    else: isinteraction = True
    if get_guild_lang(ctx.guild) == "ru":
        notexist = "Такой страницы не существует!"
        deleted = "Удаленные сообщения"
        by = "от"
        attachments = "Приклепленные файлы"
        embed2 = "Эмбед"
        nodesc = "Без описания"
        sent = "Отправлено"
        deleted2 = "Удалено"
    else:
        notexist = "This page does not exist!"
        deleted = "Deleted messages"
        by = "by"
        attachments = "Attachments"
        embed2 = "Embed"
        nodesc = "No description"
        sent = "Sent"
        deleted2 = "Deleted"
    cur.execute(f"SELECT * FROM msgs WHERE guild_id = {ctx.guild.id}")
    raw = cur.fetchall()
    try:
        m = raw[page-1]
    except IndexError:
        if isinteraction: await send(embed=discord.Embed(title=notexist), ephemeral=True)
        else: await send(embed=discord.Embed(title=notexist))
        return
    embed = discord.Embed(
        title=deleted,
        description=f"{m[0][:4000]} - {by} <@{m[2]}>",
        color=discord.Colour(m[5])
    )
    attach = ", ".join(eval_(m[6]))
    if m[10] and not m[9]:
        embed.add_field(name=embed2, value=m[10][:1024])
    if m[9] and not m[10]:
        embed.add_field(name=m[9], value=nodesc)
    if m[9] and m[10]:
        embed.add_field(name=m[9], value=m[10][:1024])
    if attach:
        embed.add_field(name=attachments, value=attach[:-2])
    embed.add_field(name=sent, value=f"<t:{m[8]}:f>")
    embed.add_field(name=deleted2, value=f"<t:{m[7]}:f>", inline=True)
    embed.set_footer(text=f"{member.name} · {page}/{len(raw)}")
    embed.set_author(name=m[4], icon_url=m[3])
    view = discord.ui.View(timeout=None)
    add = view.add_item
    button = discord.ui.Button
    add(button(label="", emoji="◀", custom_id=f"goto {page-1} {member.id}"))
    add(button(label="", emoji="▶", custom_id=f"goto {page+1} {member.id}", row=0))
    add(button(label="", emoji="🗑", row=0, style=ButtonStyle.red, custom_id=f"delete 1 {member.id}"))
    add(button(label="", emoji="🧹", row=0, style=ButtonStyle.red, custom_id=f"delete -1 {member.id}"))
    await edit(embed=embed, view=view)
class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    @command(aliases=["c", "s", "с", "снайп"], description="Shows deleted messages")
    async def snipe(self, ctx: commands.Context, page: int=1):
        await showpage(ctx.author, ctx, page, ctx.send)
    @commands.Cog.listener()
    async def on_message_delete(self, msg: discord.Message):
        cur.execute("""CREATE TABLE IF NOT EXISTS msgs(
            content TEXT, 
            guild_id INTEGER,
            user_id INTEGER,
            user_avatar TEXT,
            user_name TEXT,
            user_color INTEGER,
            attachments TEXT,
            deleted_at INTEGER,
            created_at INTEGER,
            embed_title TEXT,
            embed_desc TEXT
        )""")
        cur.execute("SELECT * FROM msgs ORDER BY rowid DESC LIMIT 1")
        if not (msg.channel.is_nsfw() or msg.content == cur.fetchall()[0][0]):
            cur.execute("INSERT INTO msgs VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                msg.content, 
                msg.guild.id, 
                msg.author.id, 
                msg.author.display_avatar.url if msg.author.display_avatar else msg.author.avatar.url, 
                msg.author.display_name, 
                msg.author.colour.value,
                str([a.url for a in msg.attachments]),
                int(time.time()),
                int(msg.created_at.timestamp()),
                msg.embeds[0].title if msg.embeds else None,
                msg.embeds[0].description if msg.embeds else None)
            )
            conn.commit()
    # @commands.Cog.listener()
    # async def on_message_edit(self, msg1: discord.Message, msg2: discord.Message):
    #     cur.execute("""CREATE TABLE IF NOT EXISTS msgs(
    #         msg1 TEXT, 
    #         msg2 TEXT, 
    #         guild_id INTEGER,
    #         guild_name INTEGER,
    #         user_id INTEGER,
    #         user_avatar TEXT,
    #         user_name TEXT,
    #         user_color INTEGER,
    #         attachments1 TEXT,
    #         attachments2 TEXT,
    #         modified_at INTEGER,
    #         embed_title1 TEXT,
    #         embed_desc1 TEXT,
    #         embed_title2 TEXT,
    #         embed_desc2 TEXT
    #     )""")
    #     if not msg1.channel.is_nsfw() and not (msg1.content == msg2.content and not (msg1.content and msg2.content)):
    #         cur.execute("INSERT INTO msgs VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
    #             msg1.content, 
    #             msg2.content, 
    #             msg1.guild.id, 
    #             msg1.guild.name, 
    #             msg1.author.id, 
    #             msg1.author.display_avatar.url if msg1.author.display_avatar else msg1.author.avatar.url, 
    #             msg1.author.display_name, 
    #             msg1.author.colour.value,
    #             str([a.url for a in msg1.attachments]),
    #             str([a.url for a in msg2.attachments]),
    #             int(time.time()),
    #             msg1.embeds[0].title if msg1.embeds else None,
    #             msg1.embeds[0].description if msg1.embeds else None,
    #             msg2.embeds[0].title if msg1.embeds else None,
    #             msg2.embeds[0].description if msg1.embeds else None)
    #         )
    #         conn.commit()
    @commands.Cog.listener("on_interaction")
    async def on_browse(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            send = interaction.response.send_message
            option = str(interaction.data.get('custom_id', False))
            if option:
                if option.startswith("delete"):
                    v = option.split(" ")
                    page = int(v[1])
                    user = int(v[2])
                    if chk(interaction.user.id, user):
                        if interaction.user.guild_permissions.manage_messages or iscreator(interaction.user.id):
                            try:
                                if page == -1:
                                    cur.execute(f"DELETE FROM msgs WHERE guild_id = {interaction.guild.id}")
                                else:
                                    cur.execute(f"DELETE FROM msgs WHERE rowid IN (SELECT rowid FROM msgs WHERE guild_id = {interaction.guild.id} LIMIT 1 OFFSET {page-1})")
                            except:
                                await send(f"{x} Не удалось удалить сообщение", ephemeral=True)
                            conn.commit()
                            await interaction.response.send_message("✅Успешно удалено", ephemeral=True)
                    else:
                        await send(f"{x} Вы не отправляли команду!", ephemeral=True)
                if option.startswith("goto"):
                    try:
                        await showpage(interaction.user, interaction, int(option.split(" ")[1]), interaction.response.send_message, interaction.response.edit_message)
                    except Exception as e: print(e)
async def setup(bot):
    await bot.add_cog(Snipe(bot))