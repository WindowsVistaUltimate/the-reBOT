import discord, psutil, os, sys
from discord.ext import commands
from botik import iscreator
from asyncio import sleep
from botik import x
from datetime import timedelta as time
from time import time as timeint
from cogs.lang import get_guild_lang
runtime = int(timeint())
def format_time(seconds, lang):
    if seconds < 60: 
        if lang == "ru": return f"{seconds} секунд"
        if lang == "en": return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        seconds = seconds - (minutes * 60)
        if lang == "ru":
            return f"{minutes} минут{f', {seconds} секунд' if seconds else ''}"
        if lang == "en": 
            return f"{minutes} minutes{f', {seconds} seconds' if seconds else ''}"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        minutes = int((seconds - (hours * 3600)) / 60)
        seconds = seconds - (minutes * 60) - (hours * 3600)
        if lang == "ru":
            return f"{hours} часов{f', {minutes} минут' if minutes else ''}{f', {seconds} секунд' if seconds else ''}"
        if lang == "en": 
            return f"{hours} hours{f', {minutes} minutes' if minutes else ''}{f', {seconds} seconds' if seconds else ''}"
    else:
        days = int(seconds / 86400)
        hours = int((seconds - (days * 86400)) / 3600)
        minutes = int((seconds - (hours * 3600) - (days * 86400)) / 60)
        seconds = seconds - (minutes * 60) - (hours * 3600) - (days * 86400)
        if lang == "ru":
            return f"{days} дней{f', {hours} часов' if hours else ''}{f', {minutes} минут' if minutes else ''}{f', {seconds} секунд' if seconds else ''}"
        if lang == "en": 
            return f"{days} days{f', {hours} hours' if hours else ''}{f', {minutes} minutes' if minutes else ''}{f', {seconds} seconds' if seconds else ''}"
class Moderationn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()
    @commands.hybrid_command(description="Creates a backup of a server")
    async def backup(self, ctx: commands.Context):
        # bak = {"channels": [], "roles": []}
        # for a in ctx.guild.categories:
        #     bak["channels"].append({a.name: [b.name for b in a.channels]})
        # bak["roles"] = [a.name for a in ctx.guild.roles]
        # await ctx.send(str(bak)[:3999])
        await ctx.send("Can't")
    @commands.hybrid_command(description="Deletes all of the roles and channels, that match a specified name. Useful for removing crash channels")
    async def delall(self, ctx: commands.Context, match):
        if ctx.author.guild_permissions.administrator or iscreator(ctx.author.id):
            if get_guild_lang(ctx.guild) == "ru": deleting = "Удаление ролей и каналов..."
            else: deleting = "Deleting roles and channels..."
            msg = await ctx.send(deleting)
            for a in await ctx.guild.fetch_roles():
                if match in a.name:
                    await a.delete()
            for a in await ctx.guild.fetch_channels():
                if match in a.name:
                    await a.delete()
            await msg.delete
    @commands.hybrid_command(aliases=["бан"], description="Bans user")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, m: discord.User, duration = None, *, reason="No"):
        if not ctx.guild: ...
        if get_guild_lang(ctx.guild) == "ru": 
            noperms = f"{x} Бот не может его забанить"
            selfban = f"{x} Вы не можете забанить себя"
            title = f"{x} Некорректный синтаксис!"
            desc = "Синтаксис: `$ban <Юзер> <Число><с|м|ч|д (секунды|минуты|часы|дни)> <Причина>`"
            banned = "{} забанен! Причина: {}"
            banned2 = '{}, ты был забанен с сервера `{}` на {}! причина: {}'
            lang = "ru"
            autounban = "Автоматический разбан"
        else: 
            noperms = f"{x} Bot have no permissions"
            selfban = f"{x} You can't ban yourself"
            title = f"{x} Wrong syntax!"
            desc = "Syntax: `$ban <User> <Number><s|m|h|d (seconds|minutes|hours|days)> <Reason>`"
            banned = "{} has been banned! Reason: {}"
            banned2 = '{}, you have been banned from a server called `{}` for {}! Reason: {}'
            lang = "en"
            autounban = "Auto-Unban"
        if m.id == ctx.author.id:
            await ctx.send(embed=discord.Embed(description=selfban))
            return
        time = 0
        try: await ctx.guild.ban(m, reason=reason)
        except:
            await ctx.send(embed=discord.Embed(description=noperms))
            return
        else:
            await ctx.send(embed=discord.Embed(description=banned.format(m, reason)))
            try: await m.send(embed=discord.Embed(description=banned2.format(m.mention, ctx.guild.name, format_time(duration, lang), reason)))
            except: pass
            if duration:
                time = duration[:-1]
                if time.isdigit(): time = int(time)
                else: await ctx.send(embed=discord.Embed(title=title, description=desc))
                match duration[0]:
                    case "s" | "с": pass
                    case "м" | "m": time *= 60
                    case "h" | "ч": time *= 3600
                    case "d" | "д": time *= 86400
                await sleep(time)
                try: await m.unban(reason=autounban)
                except: pass
    @commands.hybrid_command(aliases=["баны"], description="Баны")
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx: commands.Context):
        if not ctx.guild: ...
        if get_guild_lang(ctx.guild) == "ru": bans = "Баны"
        else: bans = "Bans"
        await ctx.send(embed=discord.Embed(title=bans, description="\n".join([a.user.mention async for a in ctx.guild.bans(limit=100)])))
    @commands.hybrid_command(description="Kicks user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, m: discord.Member, *, reason="No"):
        if m.top_role.position > ctx.author.top_role.position: ...
        if get_guild_lang(ctx.guild) == "ru": 
            noperms = f"{x} Бот не может его кикнуть"
            selfkick = f"{x} Вы не можете кикнуть себя"
            kicked = "{} кикнут! Причина: {}"
            kicked2 = '{}, вы были кикнуты с сервера `{}`! Причина: {}'
        else: 
            noperms = f"{x} Bot have no permissions"
            selfkick = f"{x} You can't kick yourself"
            kicked = "{} has been kicked! Reason: {}"
            kicked2 = '{}, you have been kicked from a server called `{}`! Reason: {}'
        if not ctx.guild: ...
        m = ctx.guild.fetch_member(m.id)
        if m.id == ctx.author.id:
            await ctx.send(embed=discord.Embed(description=selfkick))
            return
        try: await ctx.guild.kick(m, reason=reason)
        except:
            await ctx.send(embed=discord.Embed(description=noperms))
            return
        try: await m.send(embed=discord.Embed(description=kicked2.format(m.mention, ctx.guild.name, reason)))
        except: ...
        await ctx.send(embed=discord.Embed(description=kicked.format(m, reason)))
    @commands.hybrid_command(description="Слоумод")
    @commands.has_permissions(manage_guild=True)
    async def slowmode(self, ctx: commands.Context, t: int, reason="No"):
        try:
            await ctx.channel.edit(slowmode_delay=t, reason=reason)
            if ctx.interaction: await ctx.interaction.response.defer()
        except:
            if get_guild_lang(ctx.guild) == "ru": 
                await ctx.send(embed=discord.Embed(description=f"{x} Не удалось поставить слоумод"))
            else:
                await ctx.send(embed=discord.Embed(description=f"{x} Can't set slowmode"))
    @commands.hybrid_command(aliases=["мьют", "мут"], description="Заглушивает пользователя")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx: commands.Context, m: discord.Member, duration, *, reason="No"):
        if m.top_role.position > ctx.author.top_role.position: ...
        if not ctx.guild: ...
        m = ctx.guild.fetch_member(m.id)
        if get_guild_lang(ctx.guild) == "ru": 
            f"{x} Бот не может его замьютить"
            selfmute = f"{x} Вы не можете мутнуть себя"
            title = f"{x} Некорректный синтаксис!"
            desc = "Синтаксис: `$mute <Юзер> <Число><с|м|ч|д (секунды|минуты|часы|дни)> <Причина>`"
        else: 
            noperms = f"{x} Bot have no permissions"
            selfmute = f"{x} You can't mute yourself"
            title = f"{x} Wrong syntax!"
            desc = "Syntax: `$mute <User> <Number><s|m|h|d (seconds|minutes|hours|days)> <Reason>`"
        if m.id == ctx.author.id:
            await ctx.send(embed=discord.Embed(description=selfmute))
            return
        try:
            inta = int(duration[:-1])
        except:
            await ctx.send(embed=discord.Embed(title=title, description=desc))
        try:
            match duration[-1]:
                case "s"|"с": await m.timeout(time(seconds=inta), reason=reason)
                case "м"|"m": await m.timeout(time(minutes=inta), reason=reason)
                case "h"|"ч": await m.timeout(time(hours=inta), reason=reason)
                case "d"|"д": await m.timeout(time(days=inta), reason=reason)
        except:
            await ctx.send(embed=discord.Embed(description=noperms))
    @commands.hybrid_command(description="Unmutes user")
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx: commands.Context, m: discord.Member, *, reason="No"):
        if m.top_role.position > ctx.author.top_role.position: ...
        if get_guild_lang(ctx.guild) == "ru": noperms = f"{x} Бот не может его размьютить"
        else: noperms = f"{x} Bot have no permissions"
        try: await m.timeout(None, reason=reason)
        except: await ctx.send(embed=discord.Embed(description=noperms))
    @commands.has_permissions(ban_members=True)
    @commands.hybrid_command(description="Unbans user")
    async def unban(self, ctx: commands.Context, m: discord.Member, *, reason="No"):
        if get_guild_lang(ctx.guild) == "ru": noperms = f"{x} Бот не может его разбанить"
        else: noperms = f"{x} Bot have no permissions"
        try: await m.unban(reason=reason)
        except: await ctx.send(embed=discord.Embed(description=noperms))
    @commands.hybrid_command(aliases=["инфо", "сервер", "server", "guild"], description="Server info")
    async def info(self, ctx: commands.Context):
        this = ctx.guild
        if get_guild_lang(ctx.guild) == "ru":
            title = f"Информация о сервере {this.name}"
            desc = (f"Участники: {this.member_count}\n" + 
                f"Роли: {len(this.roles)}\n" +
                f"Высшая роль: {this.roles[-1].mention}\n" + 
                f"Нисшая роль: {this.roles[1].mention}\n" + 
                f"Владелец: {this.owner.mention}\n" +
                f"Боты: {len([True for i in this.members if i.bot])}\n" + 
                f"Люди: {len([True for i in this.members if not i.bot])}\n" +
                f"Баны: {len([True async for a in this.bans()])}")
        else:
            title = f"Info of the server {this.name}"
            desc = (f"Members: {this.member_count}\n" + 
                f"Roles: {len(this.roles)}\n" +
                f"Highest role: {this.roles[-1].mention}\n" + 
                f"Lowest role: {this.roles[1].mention}\n" + 
                f"Owner: {this.owner.mention}\n" +
                f"Bots: {len([True for i in this.members if i.bot])}\n" + 
                f"People: {len([True for i in this.members if not i.bot])}\n" +
                f"Bans: {len([True async for a in this.bans()])}")
        await ctx.send(embed=discord.Embed(title=title, description=desc))
    @commands.hybrid_command(description="Bot stats")
    async def botstats(self, ctx: commands.Context):
        process = psutil.Process(os.getpid())
        pr_mem = int(process.memory_info().rss / 1024 / 1024)
        mem = psutil.virtual_memory()
        total = int(mem.total / 1024 / 1024)
        used = int(mem.used / 1024 / 1024)
        if get_guild_lang(ctx.guild) == "ru":
            title = "Информация о боте"
            desc = (f"Участников серверов, в которых бот: {len(self.bot.users)}\n" + 
                f"Серверов: {len(self.bot.guilds)}\n" +
                f"Последний онлайн: <t:{last_online}:F>, <t:{last_online}:R>\n" +
                f"Время запуска: <t:{runtime}:F>, <t:{runtime}:R>\n" +
                f"Занятая оперативная память: {pr_mem} МБ / {total - used + pr_mem} МБ\n" +
                f"Общая занятая оперативная память: {used} МБ / {total} МБ\n" +
                f"Библиотека: discord.py {discord.__version__} (Python {sys.version.split(' ')[0]})")
        else:
            title = "Bot info"
            desc = (f"Users in servers with a bot: {len(self.bot.users)}\n" + 
                f"Servers: {len(self.bot.guilds)}\n" +
                f"Last online: <t:{last_online}:F>, <t:{last_online}:R>\n" +
                f"Runtime: <t:{runtime}:F>, <t:{runtime}:R>\n" +
                f"Used RAM: {pr_mem} MB / {total - used + pr_mem} MB\n" +
                f"Total used RAM: {used} MB / {total} MB\n" +
                f"Library: discord.py {discord.__version__} (Python {sys.version.split(' ')[0]})")
        await ctx.send(embed=discord.Embed(title=title, description=desc))
    @commands.hybrid_command(description="Automod")
    async def automod(self, ctx: commands.Context, pattern): ...
        #if not ctx.me.guild_permissions.manage_guild: await ctx.send("❌"); return
        #await ctx.guild.create_automod_rule(enabled=True, )
    @commands.Cog.listener("on_ready")
    async def on_uptime(self):
        global last_online
        last_online = int(timeint())
        while True:

            await sleep(1)
async def setup(bot):
    await bot.add_cog(Moderationn(bot))