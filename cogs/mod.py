import discord, psutil, os, sys
from discord.ext import commands
from botik import iscreator
from asyncio import sleep
from botik import x
from datetime import timedelta as time
from time import time as timeint
runtime = int(timeint())
class Moderationn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()
    @commands.hybrid_command(description="Делает бэкап сервера")
    async def backup(self, ctx: commands.Context):
        # bak = {"channels": [], "roles": []}
        # for a in ctx.guild.categories:
        #     bak["channels"].append({a.name: [b.name for b in a.channels]})
        # bak["roles"] = [a.name for a in ctx.guild.roles]
        # await ctx.send(str(bak)[:3999])
        await ctx.send("Нельзя")
    @commands.hybrid_command(description="Удаляет все роли и каналы с указанным названием. Полезно для удаления краш каналов.")
    async def delall(self, ctx: commands.Context, match):
        if ctx.author.guild_permissions.administrator or iscreator(ctx.author.id):
            await ctx.send("Удаление ролей и каналов...")
            for a in await ctx.guild.fetch_roles():
                if match in a.name:
                    await a.delete()
            for a in await ctx.guild.fetch_channels():
                if match in a.name:
                    await a.delete()
    @commands.hybrid_command(aliases=["бан"], description="Банит пользователя")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, m: discord.User, duration = None, *, reason="No"):
        if m.id == ctx.author.id:
            await ctx.send(embed=discord.Embed(description=f"{x} Вы не можете забанить себя"))
            return
        time = 0
        try: await ctx.guild.ban(m, reason=reason)
        except:
            await ctx.send(embed=discord.Embed(description=f"{x} Бот не может его забанить"))
            return
        else:
            await ctx.send(embed=discord.Embed(description=f'{m} забанен! Причина: {reason}'))
            try: await m.send(embed=discord.Embed(description=f'{m.mention}, ты был забанен! причина: {reason}'))
            except: pass
            if duration:
                time = duration[:-1]
                if time.isdigit(): time = int(time)
                else: await ctx.send(embed=discord.Embed(title=f"{x} Некорректный синтаксис!", description="Синтаксис: `$mute <Юзер> <Число><с|м|ч|д (секунды|минуты|часы|дни)> <Причина>`"))
                match duration[0]:
                    case "s" | "с": pass
                    case "м" | "m": time *= 60
                    case "h" | "ч": time *= 3600
                    case "d" | "д": time *= 86400
                await sleep(time)
                try: await m.unban(reason="автоматический разбан")
                except: pass
    @commands.hybrid_command(aliases=["баны"], description="Баны")
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx: commands.Context):
        await ctx.send(embed=discord.Embed(title="Баны", description="\n".join([a.user.mention async for a in ctx.guild.bans(limit=100)])))
    @commands.hybrid_command(description="Выгоняет пользователя")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, m: discord.User, *, reason="No"):
        if m.id == ctx.author.id:
            await ctx.send(embed=discord.Embed(description=f"{x} Вы не можете кикнуть себя"))
            return
        try: await ctx.guild.kick(m, reason=reason)
        except:
            await ctx.send(embed=discord.Embed(description=f"{x} Недостаточно прав у бота"))
            return
        try: await m.send(embed=discord.Embed(description=f'{m.mention}, ты был кикнут! причина: {reason}'))
        except: ...
        await ctx.send(embed=discord.Embed(description=f'{m} кикнут! Причина: {reason}'))
    @commands.hybrid_command(description="Слоумод")
    @commands.has_permissions(manage_guild=True)
    async def slowmode(self, ctx: commands.Context, t: int, reason="No"):
        try:
            await ctx.channel.edit(slowmode_delay=t, reason=reason)
        except:
            await ctx.send(embed=discord.Embed(description=f"{x} Не удалось поставить слоумод"))
    @commands.hybrid_command(aliases=["мьют", "мут"], description="Заглушивает пользователя")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, m: discord.Member, duration, *, reason="No"):
        if m.id == ctx.author.id:
            await ctx.send(embed=discord.Embed(description=f"{x} Вы не можете мутнуть себя"))
            return
        try:
            inta = int(duration[:-1])
        except:
            await ctx.send(embed=discord.Embed(title=f"{x} Некорректный синтаксис!", description="Синтаксис: `$mute <Юзер> <Число><с|м|ч|д (секунды|минуты|часы|дни)> <Причина>`"))
        try:
            match duration[-1]:
                case "s"|"с": await m.timeout(time(seconds=inta), reason=reason)
                case "м"|"m": await m.timeout(time(minutes=inta), reason=reason)
                case "h"|"ч": await m.timeout(time(hours=inta), reason=reason)
                case "d"|"д": await m.timeout(time(days=inta), reason=reason)
        except:
            await ctx.send(embed=discord.Embed(description=f"{x} Недостаточно прав у бота"))
    @commands.hybrid_command(description="Отглушивает пользователя")
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason="No"):
        try: await member.timeout(None, reason=reason)
        except: await ctx.send(embed=discord.Embed(description=f"{x} Недостаточно прав у бота"))
    @commands.hybrid_command(description="Разбанивает пользователя")
    async def unban(self, ctx: commands.Context, member: discord.Member, *, reason="No"):
        if ctx.author.guild_permissions.ban_members or iscreator(ctx.author.id):
            try: await member.timeout(None, reason=reason)
            except: await ctx.send(embed=discord.Embed(description=f"{x} Недостаточно прав у бота"))
    @commands.hybrid_command(aliases=["инфо", "сервер", "server", "guild"], description="Инфо о сервере")
    async def info(self, ctx: commands.Context):
        this = ctx.guild
        await ctx.send(
            embed=discord.Embed(
                title=f"Информация о сервере {this.name}",
                description=
                f"Участники: {this.member_count}\n" + 
                f"Роли: {len(this.roles)}\n" +
                f"Высшая роль: {this.roles[-1].mention}\n" + 
                f"Нисшая роль: {this.roles[1].mention}\n" + 
                f"Владелец: {this.owner.mention}\n" +
                f"Боты: {len([True for i in this.members if i.bot])}\n" + 
                f"Люди: {len([True for i in this.members if not i.bot])}\n" +
                f"Баны: {len([True async for a in this.bans()])}"
            )
        )
    @commands.hybrid_command(description="Статисктика о боте")
    async def botstats(self, ctx: commands.Context):
        process = psutil.Process(os.getpid())
        pr_mem = int(process.memory_info().rss / 1024 / 1024)
        mem = psutil.virtual_memory()
        total = int(mem.total / 1024 / 1024)
        used = int(mem.used / 1024 / 1024)
        await ctx.send(
            embed=discord.Embed(
                title=f"Информация о боте",
                description=
                f"Участников серверов, в которых бот: {len(self.bot.users)}\n" + 
                f"Серверов: {len(self.bot.guilds)}\n" +
                f"Последний онлайн: <t:{last_online}:F>, <t:{last_online}:R>\n" +
                f"Время запуска: <t:{runtime}:F>, <t:{runtime}:R>\n" +
                f"Занятая оперативная память: {pr_mem} МБ / {total - used + pr_mem} МБ\n" +
                f"Общая занятая оперативная память: {used} МБ / {total} МБ\n" +
                f"Библиотека: discord.py {discord.__version__} (Python {sys.version.split(' ')[0]})"
            )
        )
    @commands.hybrid_command(description="Автомод")
    async def automod(self, ctx: commands.Context, pattern): ...
        #if not ctx.me.guild_permissions.manage_guild: await ctx.send("❌"); return
        #await ctx.guild.create_automod_rule(enabled=True, )
    @commands.Cog.listener("on_ready")
    async def on_uptime(self):
        global last_online
        last_online = int(timeint())
async def setup(bot):
    await bot.add_cog(Moderationn(bot))