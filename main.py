import random
import sqlite3
import discord
import schedule
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands, tasks
from discord.ext.commands import *
from discord.utils import get
from discord.ui import Button, View
from youtube_dl import YoutubeDL
import asyncio
"""                                                                            Конфиг Бота                                                                                            """
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=discord.Intents().all())  # Параметр Бот
client = discord.Client
Token = "MTAyNzkyNjA1NjA1NDgzNzMyOQ.Geh_vr.dFSQ9bAPmfZ1Hz6yUB3XurSgmRfX-liQvvUuJA"  # Токен Бота
ROLES = {}  # Все роли сервера
MAX_ROLES_PER_USER = 999  # Максимальное кол-во ролей у человека
DATABASE = "serverdruzey3.db"
EMBED_COLOR = "#6140c7"
# ROLES ID
IN_WL_ROLE = 1027274244465381387 # Роль человека в Whitelist
NOT_IN_WL_ROLE = 1027274595285352598 # Роль человека не в Whitelist
MODERATOR_ROLE = 1027275443293917225 # Роль модератора сервера
ADMIN_ROLE = 1043145669323522139 # Роль администратора сервера
CHAT_CREATED_ROLE = 1057728517212745758
# Сделать роль модератора и администратора, поменять все остальное.

# CHANNELS ID
SERVER_ID = 1027270366592253973
PROXOD_ID = 1027277592904077362
VOICE_CATEGORY = 1027273988528930826

"""                                                                              Код Бота                                                                                             """
#  Текстовое Сообщение при заходе на сервер
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1027276732476182568)
    embed = discord.Embed(
        title="К нам зашел новый человек!",
        description=f"**{member.mention} Добро пожаловать в '{member.guild.name}'**\n\n"
                    f"**Чтобы начать играть на сервере нужно:**\n"
                    f"**1. Ознакомиться с описание сервера <#1027276936470331473>**\n"
                    f"**2. Ознакомиться с ролями сервера <#1027277168155316254>**\n"
                    f"**3. Написать заявку по форме <#1027277592904077362>**\n"
                    f"**Рекомендуем разрешить сообщения от участников сервера, чтобы с вами можно было связаться!**",
        colour=discord.Colour.from_str(EMBED_COLOR)
    )
    await channel.send(embed=embed)

    guild = bot.get_guild(SERVER_ID)
    role = guild.get_role(NOT_IN_WL_ROLE)
    await member.add_roles(role)


# Выдача роли по эмодзи(Только администраторы!)
@bot.event
async def on_raw_reaction_add(payload):
    # Подключение к Базе Данных
    connect = sqlite3.connect(DATABASE)
    cursor = connect.cursor()
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    moderator_role = discord.utils.get(message.guild.roles, id=MODERATOR_ROLE)
    admin_role = discord.utils.get(message.guild.roles, id=ADMIN_ROLE)
    member = payload.member

    guild = bot.get_guild(SERVER_ID)
    role = guild.get_role(IN_WL_ROLE)
    remove_role = guild.get_role(NOT_IN_WL_ROLE)
    if str(payload.emoji) == '✅' and moderator_role in member.roles or admin_role in member.roles and channel.id == PROXOD_ID:
        await message.author.add_roles(role)
        await message.author.remove_roles(remove_role)
        embed = discord.Embed(
            title="Вы добавлены в белый список сервера!",
            description=f"**{message.author.mention} Теперь вы можете играть на нашем сервере!**\n\n"
                        f"**Как зайти на сервер?**\n"
                        f"**1.Посмотрите инструкцию: https://www.youtube.com/watch?v=ma22SXV1Kvo**\n"
                        f"**2.Введите данные сервера:**\n"
                        f"**Ip:**127.0.0.1**\n"
                        f"**Port:**33000**\n\n"
                        f"**!команды - Список всех команд для бота**\n",

            colour=discord.Colour.from_str(EMBED_COLOR)
        )
        user_id = message.author.id
        user_name = message.author
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        cursor.execute(f"UPDATE users SET user_name = '{user_name}' WHERE user_id = {user_id}")
        cursor.execute("UPDATE users SET user_bank = 0 WHERE user_id = ?", (user_id,))
        cursor.close()
        connect.commit()
        connect.close()
        await message.author.send(embed=embed)
    
    if str(payload.emoji) == '⛔' and moderator_role in member.roles or admin_role in member.roles:
        await message.delete()


#  Выдача роли когда убирается эмодзи
@bot.event
async def on_raw_reaction_remove(payload):
    channel = bot.get_channel(PROXOD_ID)
    message = await channel.fetch_message(payload.message_id)
    guild = bot.get_guild(SERVER_ID)
    role = guild.get_role(IN_WL_ROLE)
    remove_role = guild.get_role(NOT_IN_WL_ROLE)

    moderator_role = discord.utils.get(message.guild.roles, id=MODERATOR_ROLE)
    admin_role = discord.utils.get(message.guild.roles, id=ADMIN_ROLE)
    member = await (await bot.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)

    if str(payload.emoji) == '✅' and moderator_role in member.roles or admin_role in member.roles:
        await message.author.add_roles(remove_role)
        await message.author.remove_roles(role)


# Команда Помощь
@bot.command()
async def Помощь(ctx):
    embed = discord.Embed(
        title="Информация о сервере:",
        description=f"**<#1027277975961485392> - Новости сервера**\n"
                    f"**<#1027278038066536648> - Описание сервера**\n"
                    f"**<#1027278328685658112> - Роли сервера**\n"
                    f"**<#1027278543983476757> - Полезные ссылки**\n"
                    f"**<#1027915807507894374> - Поддержка сервер(Помощь игрокам)**\n\n"
                    f"**!команды - Список всех команд для бота**\n",

        colour=discord.Colour.from_str(EMBED_COLOR)
    )
    await ctx.reply(embed=embed)


# Информация по игровому серверу
@bot.command()
async def Сервер(ctx):
    embed = discord.Embed(
        title="Данные сервера; Инструкция по заходу",
        description=f"**Данные Сервера:**\n"
                    f"**Ip:**\n"
                    f"**Port:**\n\n"
                    f"**Туториал**\n"
                    f"**https://www.youtube.com/watch?v=ma22SXV1Kvo**",

        colour=discord.Colour.from_str(EMBED_COLOR)
    )
    await ctx.reply(embed=embed)


# Отправленние обновленных сообщений в каналы(Роли, Описание, Ссылки)
@bot.command()
async def Setup(ctx):

    channel_decription1 = bot.get_channel(1027276936470331473)
    channel_decription2 = bot.get_channel(1027278038066536648)
    channel_roles1 = bot.get_channel(1027277168155316254)
    channel_roles2 = bot.get_channel(1027278328685658112)
    channel_links = bot.get_channel(1027278543983476757)
    channel_proxod = bot.get_channel(1027277592904077362)
    # Отправка в Описание1
    admin_role = discord.utils.get(ctx.guild.roles, id=ADMIN_ROLE)
    if admin_role in ctx.author.roles:
        decription = discord.Embed(
                title="ОПИСАНИЕ И ИСТОРИЯ СЕРВЕРА SD",
                description=f"**SD(Server Druzey ) Берет свое начало еще в октябре 2021 года, когда группа друзей начала совместное выживание. Я загорелся желанием расширить нашу игру.**\n\n"
                            f"**Сначала мы играли на Minecraft Realms, нас играло менее 10 человек, я захотел создать свою команду, искал людей, приглашал их играть на нашем сервере вместе со мной, но они приходили и играли сами по себе, что было хорошо, но было проблематично мне. И так нас набралось около 10 человек, 8 человек стабильно играло каждый день. После этого мы построили город, коммуницировали, торговали, веселились, но все закончилось тем, что мы закрыли наш первый «сезон» залив все лавой и сохранив приятные видеозаписи нашей игры.**\n\n"
                            f"**Спустя несколько месяцев мы снова загорелись желанием играть в майнкрафт, я сделал дискорд, искал людей, и в итоге нас набралось более 25 человек. Мы с друзьями радовались, что у нас будет больше возможностей и игровых моментов, но в первый день были технические проблемы, которые расстроили некоторых игроков и по итогу нас осталось около 18 человек. Мы построили разные города, торговали, пару раз повоевали. Так и закончился 2 «сезон» нашего сервера. Хочу подметить, что мы брали за основу и как пример одноименный сервер «MineShield» и старались сделать, что-то подобное, но со своей изюминкой**\n\n"
                            f"**И вот, я - главный технический администратор, который следил за хостингов и настраивал все, делал оформление, все для наилучшего игрового процесса, параллельно учился кодингу и научился созданию несложных вебсайтов как сайт нашего сервера, а также Discord, Telegram ботов, решил сделать новый «сезон» нашего сервера со своими друзьями!**\n\n"
                            f"**До встречи на открытии сервера, заполним информацию по 3 «сезону» вместе с вами) Удачи!**",
                colour=discord.Colour.from_str(EMBED_COLOR),
                
            )
        decription.set_image(url="https://cdn.discordapp.com/attachments/1027281849023729665/1055575435515285534/4ec60285a7de7a16.png")


        roles = discord.Embed(
        title="РОЛИ ДИСКОРД СЕРВЕРА И ИГРЫ:",
        description=f"**@🤠 ➤ Модератор - контролирует игроков, помогает им**\n"
                    f"**@🤖 ➤ Бот - помогают отвечать на быстрые вопросы**\n"
                    f"**@✅ ➤ ДОБАВЛЕН В WL - Игрок, который может зайти на сервер**\n"
                    f"**@❌ ➤ НЕТ В WL - Игрок, который должен пройти верификацию**\n\n"
                    f"**@💰 ➨ ПОДДЕРЖАЛ ПРОЕКТ - Поддержал финансово проект!**\n"
                    f"**@🔆➨ ОПЫТНЫЙ - Олд проекта**\n"
                    f"**@🔰 ➨ НОВИЧЕК - Новичек сервера**",
        colour=discord.Colour.from_str(EMBED_COLOR))

        links = discord.Embed(
        title="Полезные ссылки:",
        description=f"**VK GROUP: https://vk.com/serverdruzeyminecraft**\n"
                    f"**DISCORD: https://discord.gg/che47kyQXc**\n"
                    f"**КАК ЗАЙТИ(ВИДЕО): https://www.youtube.com/watch?v=ma22SXV1Kvo**\n"
                    f"**IRINQUE WEBSITE: https://irinque.ru/ (Не куплен SSL-Протокол, поэтому выводиться предупреждение, на сайте не нужно ничего вводить и тд. Сайт - безопасен!)**",
        colour=discord.Colour.from_str(EMBED_COLOR))

        proxod = discord.Embed(
        title="Форма заявки для игры на сервере:",
        description=f"**1. Никнейм PS4(Если есть, Если нет, то пишите 'Нет')**\n"
                    f"**2. Никнейм Microsoft**\n"
                    f"**3. Ваше Имя**\n"
                    f"**4. Ваш Возраст**\n"
                    f"**5. Ваш Часовой пояс**\n"
                    f"**6. Ваша игровая платформа(ПК/PS/XBOX/SWITCH/MOBILE**",
        colour=discord.Colour.from_str(EMBED_COLOR))

        await channel_decription1.send(embed=decription)
        await channel_decription2.send(embed=decription)
        await channel_roles1.send(embed=roles)
        await channel_roles2.send(embed=roles)
        await channel_links.send(embed=links)
        await channel_proxod.send(embed=proxod)

# Отправка формы заполнения заявки
@bot.command()
async def Form(ctx):
    channel_proxod = bot.get_channel(1027277592904077362)
    proxod = discord.Embed(
        title="Форма заявки для игры на сервере:",
        description=f"**1. Никнейм PS(Если есть, Если нет, то пишите 'Нет')**\n"
                    f"**2. Никнейм Microsoft**\n"
                    f"**3. Ваше Имя**\n"
                    f"**4. Ваш Возраст**\n"
                    f"**5. Ваша игровая платформа(ПК/PS/XBOX/SWITCH/MOBILE**",
        colour=discord.Colour.from_str(EMBED_COLOR))
    await channel_proxod.send(embed=proxod)

# Отправляет все команды сервера
@bot.command() 
async def Команды(ctx):
    admin_role = discord.utils.get(ctx.guild.roles, id=ADMIN_ROLE)
    moderator_role = discord.utils.get(ctx.guild.roles, id=MODERATOR_ROLE)
    admin_channel = bot.get_channel(1043244594684493954).id

    if moderator_role in ctx.author.roles and ctx.channel.id == admin_channel or admin_role in ctx.author.roles and ctx.channel.id == admin_channel:
        commands = discord.Embed(
            title=f"**Все команды сервера:**",
            description=f"**!Команды** - **Все команды сервера**\n"
                        f"**!Помощь** - **Информация о сервере**\n"
                        f"**!Сервер** - **Все данные сервера и туториал по заходу**\n"
                        f"**!Передать** - **Передать деньги другому(работает только в канале <#1042174110295408640>) Пример: '!передать @IRINQUE 10'**\n"
                        f"**!Курс** - **Узнать информацию о нынешнем курсе валюты сервера**\n\n"
                        f"**Администраторские команды:**\n"
                        f"**!Give** - **Выдать человеку валюту из банка сервера(ИСПОЛЬЗОВАТЬ БЕЗ РАЗРЕШЕНИЯ <@976511515450572830> - ЗАПРЕЩЕНО**\n"
                        f"**!Bring** - **Забрать у человека деньги(ИСПОЛЬЗОВАТЬ БЕЗ РАЗРЕШЕНИЯ <@976511515450572830> - ЗАПРЕЩЕНО**\n"
                        f"**!StartCource** - **Запустить изменение цены валюты(ИСПОЛЬЗОВАТЬ БЕЗ РАЗРЕШЕНИЯ <@976511515450572830> - ЗАПРЕЩЕНО**\n"
                        f"**!StopCource** - **Остановить изменение цены валюты(ИСПОЛЬЗОВАТЬ БЕЗ РАЗРЕШЕНИЯ <@976511515450572830> - ЗАПРЕЩЕНО**\n"
                        f"**!Clean - Удаляет все сообщения в канале**",
        colour=discord.Colour.from_str(EMBED_COLOR))
        await ctx.reply(embed=commands)
    else:
        commands = discord.Embed(
            title=f"**Все команды сервера:**",
            description=f"**!Команды** - **Все команды сервера**\n"
                        f"**!Помощь** - **Информация о сервере**\n"
                        f"**!Сервер** - **Все данные сервера и туториал по заходу**\n"
                        f"**!Передать** - **Передать деньги другому(работает только в канале <#1042174110295408640>)**\n"
                        f"**!Курс** - **Узнать информацию о нынешнем курсе валюты сервера**\n",
            colour=discord.Colour.from_str(EMBED_COLOR)
        )
        await ctx.reply(embed=commands)

@bot.command() 
async def Clean(ctx):
    admin_role = discord.utils.get(ctx.guild.roles, id=ADMIN_ROLE)
    if admin_role in ctx.author.roles:
        await ctx.channel.purge()
"""                                                                                Тех поддержка сервера                                                                                """
@bot.command()
async def SupporPanel(ctx):
    # Конфиг функции
    Support_channel = bot.get_channel(1027915807507894374)
    Support_category = get(ctx.guild.categories, id = 1027913914022903808)
    PanelMessageEmbed = discord.Embed(
        title="ОБРАЩЕНИЕ К АДМИНИСТРАЦИИ СЕРВЕРА",
        description=f"**Приветствуем, чтобы обратиться к администрации сервера, вам нужно нажать на кнопку снизу 👇**",
        colour=discord.Colour.from_str(EMBED_COLOR))
    # Отправка Сообщения 
    async def ButtonClick_OpenDialog(interaction):
        global Member
        guild = ctx.guild
        Member = interaction.user
        Admin_role = get(guild.roles, id=ADMIN_ROLE)
        Moderator_role = get(guild.roles, id=MODERATOR_ROLE)
        InSupport_Role = get(guild.roles, id=CHAT_CREATED_ROLE)
        SupportMessageEmbed = discord.Embed(
        title="Чат поддержки открыт!",
        description=f"**{interaction.user.mention} чат открыт.\nИспользуйте кнопку, чтобы управлять чатом!(Если вы все обсудили, закройте чат!)**",
        colour=discord.Colour.from_str(EMBED_COLOR))
        Owerwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        Member: discord.PermissionOverwrite(read_messages=True),
        Moderator_role: discord.PermissionOverwrite(read_messages=True),
        Admin_role: discord.PermissionOverwrite(read_messages=True)
        }
        if InSupport_Role not in Member.roles:
            CreatedSupportChannel = await interaction.guild.create_text_channel(name=f'{interaction.user.name}', category = Support_category, overwrites=Owerwrites) # Работает с методами discord.py(Как создать чат)
            await CreatedSupportChannel.send(embed=SupportMessageEmbed, view=SupportMenuButtons)
            await Member.add_roles(InSupport_Role)
    async def ButtonClick_PanelMenuClose(interaction):
        AdminMember = interaction.user
        guild = ctx.guild
        InSupport_Role = get(guild.roles, id=CHAT_CREATED_ROLE)
        await interaction.channel.delete()
        await Member.remove_roles(InSupport_Role)
        await AdminMember.remove_roles(InSupport_Role)

    admin_role = discord.utils.get(ctx.guild.roles, id=ADMIN_ROLE)
    if admin_role in ctx.author.roles:
        # Кнопка "Создать диалог"
        OpenDialog = Button(label="Открыть Диалог", style=discord.ButtonStyle.primary)
        OpenDialog.callback = ButtonClick_OpenDialog
        # Кнопка "Закрыть диалог"
        CloseDialog = Button(label="Закрыть Диалог", style=discord.ButtonStyle.danger)
        CloseDialog.callback = ButtonClick_PanelMenuClose
        SupportMenuButtons = View()
        SupportMenuButtons.add_item(CloseDialog)
        MainButtons = View()
        MainButtons.add_item(OpenDialog)
    else:
        print(f"{ctx.author} Недостаточно прав, чтобы применить данную команду!" )

    await Support_channel.send(embed=PanelMessageEmbed, view=MainButtons)
"""                                                                                Приватные Голосовые                                                                                """
@bot.event
async def on_voice_state_update(member, before, after):
    embed = discord.Embed(
            title="",
            description=f"**{member.mention}, эй, ты попытался зайти в канал сразу из своего! Перезайди в канал <#1056600260547457124>**",

            colour=discord.Colour.from_str(EMBED_COLOR)
        )
    
    global privatechannel
    server = member.guild # Получаем имя сервера
    admin_role = get(server.roles, id=ADMIN_ROLE) # Получаем админ роль
    voicecategory = get(server.categories, id = VOICE_CATEGORY) # Получаем категорию(Голосовых)
    inchat_role = get(server.roles, id=1056632566985261157)
    if after.channel and after.channel != before.channel and after.channel.name == "┠《➕》Создать" and inchat_role not in member.roles:
        privatechannel = await member.guild.create_voice_channel(name = f'{member.name}', category = voicecategory) # Создаем голосовой канал;
        await privatechannel.set_permissions(member, connect = True, mute_members = False, move_members = False, manage_channels = True) # Устанавливаем возможности;
        await member.move_to(privatechannel) # Переносим пользователя в созданный канал;
        await member.add_roles(inchat_role)

    if after.channel and after.channel != before.channel and after.channel.name == "┠《➕》Создать" and inchat_role in member.roles:
        await member.send(embed=embed)
        await member.remove_roles(inchat_role)
    if before.channel and after.channel != before.channel and before.channel.name == f"{member.name}" and inchat_role in member.roles and len(before.channel.members) == 0:
        await member.remove_roles(inchat_role)
        await privatechannel.delete()
    if privatechannel and len(privatechannel.members) == 0:
        await member.remove_roles(inchat_role)
        await privatechannel.delete()

"""                                                                                 Музыка в Боте                                                                                       """
YDL_OPTIONS = {}
@bot.command()
async def Play(ctx, url):
    await ctx.message.author.voice.channel.connect()

    with YoutubeDL(YDL_OPTIONS) as ydl:
        if "https://" in url:
            info = ydl.extract_info(url, donwload=False)
        else:
            info = ydl.extract_info(f"ytsearch: {url}", donwload=False)["entries"][0]
"""                                                                                 Работа с валютой                                                                                  """
# Команда курс
@bot.command()
async def Курс(ctx):
    connect = sqlite3.connect(DATABASE)
    cursor = connect.cursor()
    Currency = cursor.execute("SELECT standart FROM currency").fetchone()
    cursor.close()
    connect.commit()
    connect.close()
    emoji1 = discord.utils.get(bot.emojis, name='ruby')
    emoji2 = discord.utils.get(bot.emojis, name='diamond')
    embed = discord.Embed(
        title=f"**1 Коин {emoji1} = {Currency[0]} АР {emoji2}**",
        colour=discord.Colour.from_str(EMBED_COLOR)
    )
    await ctx.reply(embed=embed)

# Передача денег
@bot.command()
async def Передать(ctx, user: discord.Member, sum):
    perevodi = bot.get_channel(1042174110295408640).id
    emoji1 = discord.utils.get(bot.emojis, name='ruby')
    if ctx.channel.id == perevodi:
        connect = sqlite3.connect(DATABASE)
        cursor = connect.cursor()
        if bool(len(cursor.execute("SELECT * FROM users WHERE user_id = ?", (user.id,)).fetchall())):
            Balance_Priem = cursor.execute("SELECT user_bank FROM users WHERE user_id = ?", (user.id,)).fetchone()[0]
            Balance_Sender = cursor.execute("SELECT user_bank FROM users WHERE user_id = ?", (ctx.message.author.id,)).fetchone()[0]
            if int(Balance_Sender) - int(sum) >= 0:
                Priem = cursor.execute(f"UPDATE users SET user_bank = (user_bank + {int(sum)}) WHERE user_id = {int(user.id)}")
                Send = cursor.execute(f"UPDATE users SET user_bank = (user_bank - {int(sum)}) WHERE user_id = {ctx.message.author.id}")
                Balance_Priem = cursor.execute("SELECT user_bank FROM users WHERE user_id = ?", (user.id,)).fetchone()[0]
                Balance_Sender = cursor.execute("SELECT user_bank FROM users WHERE user_id = ?", (ctx.message.author.id,)).fetchone()[0]
                transaction = discord.Embed(
                title="✅ Новая транзакция",
                description=f"**Отправитель: {ctx.message.author.mention}**\n"
                            f"**Получатель: {user.mention}**\n"
                            f"**Переведено: {sum} {emoji1}**\n"
                            f"**Баланс Получателя: {Balance_Priem} {emoji1}**\n"
                            f"**Баланс Отправителя: {Balance_Sender} {emoji1}**",
                colour=discord.Colour.from_str(EMBED_COLOR))
                transaction_channel = bot.get_channel(1042173815930765382)
                await transaction_channel.send(embed=transaction)
                cursor.close()
                connect.commit()
                connect.close()
            else:
                transactionERROR = discord.Embed(
                title=f"❌ Ошибка перевода!",
                description=f"**У {ctx.message.author.mention} недостаточно средств для перевода!**\n"
                            f"**Баланс отправителя: {Balance_Sender} {emoji1}**\n"
                            f"**Не хватает: {(int(Balance_Sender) - int(sum)) * -1} {emoji1}**",
                colour=discord.Colour.from_str(EMBED_COLOR))
                await ctx.reply(embed=transactionERROR)
    else:
        peredatERROR = discord.Embed(
            title=f"**Ошибка перевода!**",
            description=f"Переводите, используя канал - <#1042174110295408640>",
            colour=discord.Colour.from_str(EMBED_COLOR)
        )
        await ctx.reply(embed=peredatERROR)

# Функция забрать деньги
@bot.command()
async def Bring(ctx, user: discord.Member, sum):
    moderator_role = discord.utils.get(ctx.guild.roles, id=MODERATOR_ROLE)
    admin_role = discord.utils.get(ctx.guild.roles, id=ADMIN_ROLE)
    emoji1 = discord.utils.get(bot.emojis, name='ruby')
    if moderator_role in ctx.author.roles or admin_role in ctx.author.roles:
        connect = sqlite3.connect(DATABASE)
        cursor = connect.cursor()  
        if bool(len(cursor.execute("SELECT * FROM users WHERE user_id = ?", (user.id,)).fetchall())):
            Balance = cursor.execute("SELECT user_bank FROM users WHERE user_id = ?", (user.id,)).fetchone()[0]
            if int(Balance) - int(sum) >= 0:
                cursor.execute(f"UPDATE users SET user_bank = (user_bank - {int(sum)}) WHERE user_id = {int(user.id)}")
                Balance = cursor.execute("SELECT user_bank FROM users WHERE user_id = ?", (user.id,)).fetchone()[0]
                transaction = discord.Embed(
                title="✅ Новая транзакция",
                description=f"**Забирает: БАНК**\n"
                        f"**У кого: {user.mention}**\n"
                        f"**Потрачено: {sum} {emoji1}**\n"
                        f"**Баланс: {Balance} {emoji1}**",
                colour=discord.Colour.from_str(EMBED_COLOR))
                transaction_channel = bot.get_channel(1042173815930765382)
                await transaction_channel.send(embed=transaction)
                cursor.close()
                connect.commit()
                connect.close()
            else:
                transactionERROR = discord.Embed(
                title="У пользователя не достаточно средств для снятия!",
                description=f"**Баланс пользователя: {Balance}**\n",
                colour=discord.Colour.from_str(EMBED_COLOR))
                await ctx.reply(embed=transactionERROR)

# Функция Выдать деньги
@bot.command()
async def Give(ctx, user: discord.Member, sum):
    moderator_role = discord.utils.get(ctx.guild.roles, id=MODERATOR_ROLE)
    admin_role = discord.utils.get(ctx.guild.roles, id=ADMIN_ROLE)
    emoji1 = discord.utils.get(bot.emojis, name='ruby')
    if moderator_role in ctx.author.roles or admin_role in ctx.author.roles:
        connect = sqlite3.connect(DATABASE)
        cursor = connect.cursor()
        if bool(len(cursor.execute("SELECT * FROM users WHERE user_id = ?", (user.id,)).fetchall())):
            cursor.execute(f"UPDATE users SET user_bank = (user_bank + {int(sum)}) WHERE user_id = {int(user.id)}")
            Balance = cursor.execute("SELECT user_bank FROM users WHERE user_id = ?", (user.id,)).fetchone()[0]
            transaction = discord.Embed(
            title="✅ Новая транзакция",
            description=f"**Отправитель: БАНК**\n"
                        f"**Получатель: {user.mention}**\n"
                        f"**Получено: {sum} {emoji1}**\n"
                        f"**Баланс: {Balance} {emoji1}**",
            colour=discord.Colour.from_str(EMBED_COLOR))
            transaction_channel = bot.get_channel(1042173815930765382)
            await transaction_channel.send(embed=transaction)
            cursor.close()
            connect.commit()
            connect.close()

# Таймер и изменение курса
async def graphic():
    channel = bot.get_channel(1042173661899149432)
    emoji1 = discord.utils.get(bot.emojis, name='ruby')
    emoji2 = discord.utils.get(bot.emojis, name='diamond')
    connect = sqlite3.connect(DATABASE)
    cursor = connect.cursor()
    Currency = cursor.execute("SELECT standart FROM currency").fetchone()
    number = random.randint(1, 2)
    update = random.randint(1, 3)
    if number == 1:
        cursor.execute(f"UPDATE currency SET standart = standart + {update}")
        Currency = cursor.execute("SELECT standart FROM currency").fetchone()
        embed = discord.Embed(
        title=f"**📈 Валюта поднялась в цене!**",
        description=f"**1 Коин {emoji1} = {Currency[0]} АР {emoji2}**",
        colour=discord.Colour.from_str(EMBED_COLOR)
        )
        await channel.send(embed=embed)
        
        cursor.close()
        connect.commit()
        connect.close()
                
    elif number == 2 and int(Currency[0]) - update >= 0:
        cursor.execute(f"UPDATE currency SET standart = standart - {update}")
        Currency = cursor.execute("SELECT standart FROM currency").fetchone()
        embed = discord.Embed(
        title=f"**📉 Валюта упала в цене!**",
        description=f"**1 Коиг {emoji1} = {Currency[0]} АР {emoji2}**",
        colour=discord.Colour.from_str(EMBED_COLOR)
        )
        await channel.send(embed=embed)
        
        cursor.close()
        connect.commit()
        connect.close()

# Начало курса. По команде запускается код
scheduler = AsyncIOScheduler(timezone="utc")
@bot.command()
async def StartCource(ctx):
    moderator_role = discord.utils.get(ctx.guild.roles, id=MODERATOR_ROLE)
    admin_role = discord.utils.get(ctx.guild.roles, id=ADMIN_ROLE)
    if moderator_role in ctx.author.roles or admin_role in ctx.author.roles:
        scheduler.add_job(graphic, 'interval', hours=1)
        scheduler.start()
        embed = discord.Embed(
            title="✅ Изменение курса запущено!",
            colour=discord.Colour.from_str(EMBED_COLOR)
        )
        await ctx.reply(embed=embed)

# Остановка курса. По команде биржа останавливается
@bot.command()
async def StopCource(ctx):
    moderator_role = discord.utils.get(ctx.guild.roles, id=MODERATOR_ROLE)
    admin_role = discord.utils.get(ctx.guild.roles, id=ADMIN_ROLE)
    if moderator_role in ctx.author.roles or admin_role in ctx.author.roles:
        scheduler.shutdown()
        embed = discord.Embed(
            title="⛔ Изменение курса остановлено!",
            colour=discord.Colour.from_str(EMBED_COLOR)
        )
        await ctx.reply(embed=embed)


"""                                                                                 СЕРВЕРНАЯ ЧАСТЬ                                                                                     """
# Обработка ошибок  
 
"""@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        transactionERROR = discord.Embed(
        title="Пользователь с таким ником - не найден",
        colour=discord.Colour.from_rgb(0, 162, 255))
        await ctx.reply(embed=transactionERROR)
"""


bot.run(Token)