bot = None
if __name__ == '__main__':
	from discord.ext.commands import CommandNotFound, MissingRequiredArgument, BadArgument, MissingPermissions
	from random import choice, random
	import discord, os, asyncio
	from discord.ext import commands
	from cogs.lang import get_guild_lang
	from sys import argv, stdout, stdin
	async def repl(string: str="") -> str:
		while True:
			await asyncio.get_event_loop().run_in_executor(None, lambda s=string: stdout.write(s+' '))
			result = (await asyncio.get_event_loop().run_in_executor(None, stdin.readline)).strip()
			match result:
				case "shutdown" | "s": raise SystemExit()
				case "restart" | "r": 
					os.system(f'start python "{__file__}"')
					raise SystemExit()
	if len(argv) > 1:
		if argv[1] == "--hide-window" and os.name == 'nt':
			import ctypes
			ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
	
	# -------------------------- Инициализация ---------------------------- #

	if not os.path.isdir("./database/"): os.mkdir("./database/")
	if not os.path.isdir("./database/economy/"): os.mkdir("./database/economy/")
	if not os.path.isfile("config.py"): raise SystemExit("Missing config.py")

	from config import *
	is_first_time = True
	bot = commands.Bot(
		command_prefix = prefix, 
		help_command=None, 
		intents=intents
	)
x = "<:x_:936318381244690463>"
emojis = {"x": x}
chk = lambda id, user: user == id or id == 733572313425117195 or id == 984534426656587787
iscreator = lambda id: id == 733572313425117195 or id == 984534426656587787
# guild_langs = json.loads(open("./database/langs.json", "r", encoding="utf-8").read())

# -------------------------- При ошибке ---------------------------- #

if __name__ == "__main__":
	@bot.event
	async def on_command_error(ctx: commands.Context, error):
		if get_guild_lang(ctx.guild.id) == "ru":
			fewarguments = f"{x} Отсутствует аргумент"
			typeerror = f'{x} введен неправильный тип: Нужно'
			typeerror2 = 'для параметра'
			nopermissions = choice([f"{x} Вы ни такой высокий дядька что бы эту крутую штучку делать", f"{x} Нет, тебе нельзя", f"{x} Да кто тебе позволяет???"])
			errora = "Произошла ошибка"
			typeenum = {"int": "Целое число", "str": "Текст", "float": "Целое или дробное число", "discord.Member": "Юзер", "discord.TextChannel": "Канал", "discord.Emoji": "Эмодзи"}
		else:
			fewarguments = f"{x} Too few arguments"
			typeerror = f'{x} Wrong type:'
			typeerror2 = 'is required for a parameter called'
			nopermissions = f"{x} Not enough permissions"
			errora = "Uncaught exception:"
			typeenum = {"int": "Integer", "str": "Text", "float": "Decimal", "discord.Member": "User", "discord.TextChannel": "Channel", "discord.Emoji": "Emoji"}
		match error:
			case CommandNotFound(): ...
			case MissingRequiredArgument(): await ctx.send(embed=discord.Embed(title=f"{fewarguments}: `{error.param.name}`", colour=discord.Colour.from_hsv(random(), 1, 1)))
			case BadArgument(): 
				error = str(error).split('"')
				await ctx.send(embed=discord.Embed(title=f"{typeerror} `{typeenum[error[1]]}` {typeerror2} `{error[3]}`"))
			case MissingPermissions(): await ctx.send(embed=discord.Embed(title=nopermissions, colour=discord.Colour.from_hsv(random(), 1, 1)))
			case _:
				await ctx.send(embed=discord.Embed(title=errora, description=f"```{error}```"))
				print(error, ctx.channel.name, str(ctx.author), ctx.guild.name)

# -------------------------- Чатбот ---------------------------- #
	
	# from cogs.chatbot import cur, conn
	# import re
	# @bot.tree.context_menu(name="Ответить на сообщение")
	# async def react(interaction: discord.Interaction, message: discord.Message):
	# 	filtered = re.sub(r"<(@\d+)>", r"\1", message.content).replace("@everyone", "everyone").replace("@here", "here")
	# 	filtered = re.sub(r"(https|http|ftp)://\S+", r"[ссылка]", filtered)
	# 	filtered = re.sub(r"discord.gg/\S+", r"[приглашение]", filtered)
	# 	filtered = filtered.strip()
	# 	if filtered and not message.channel.nsfw: 
	# 		cur.execute("SELECT * FROM msgs WHERE content = ?", (filtered,))
	# 		if not cur.fetchall():
	# 			cur.execute("INSERT INTO msgs(content) VALUES(?)", (filtered,))
	# 		conn.commit()
	# 	cur.execute("SELECT * FROM msgs order by RANDOM() LIMIT 1")
	# 	await interaction.response.send_message(f"> {message.content}\n{message.author.mention}{cur.fetchall()[0][0]}")

# -------------------------- Статус ---------------------------- #

	@bot.event
	async def on_ready():
		activity = discord.Game(name=f"$help | {len(bot.guilds)} servers with {len(bot.users)} people")
		await bot.change_presence(activity=activity, status=discord.Status.idle)
		if set(bot.tree.get_commands()) != set(await bot.tree.fetch_commands()): await bot.tree.sync()
		print(f"Бот онлайн! {str(bot.user)}")
		if(is_first_time == True):
			asyncio.create_task(repl())
		is_first_time == False

# -------------------------- Приветствие при входе на сервер ---------------------------- #

if __name__ == "__main__":
	@bot.event
	async def on_guild_join(guild: discord.Guild):
		langbtns = discord.ui.View(timeout=None)
		langbtns.add_item(discord.ui.Button(label="English", custom_id="lang_en"))
		langbtns.add_item(discord.ui.Button(label="Русский", custom_id="lang_ru"))
		try:
			joinchannel = guild.system_channel
			await joinchannel.send(embed=
				discord.Embed(
					title="Thanks for adding me to server!", 
					description="To begin, choose language below:"
				),
				view = langbtns
			)
		except:
			try:
				await guild.text_channels[0].send(embed=
				discord.Embed(
					title="Thanks for adding me to server!", 
					description="To begin, choose language below:"
				),
				view = langbtns)
			except:
				pass

# -------------------------- Команды и бот -------------------------------- #

	async def main(token): 
		for file in os.listdir("./cogs"):
			if file.endswith(".py"):
				await bot.load_extension('cogs.' + file[:-3])
				print(file, "loaded")
		print("starting...")
		try: await bot.start(token)
		except: raise SystemExit("Token is invalid, or can't connect to discord servers")
	while True: asyncio.run(main(token))