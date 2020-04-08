# Импортируем нужные библиотеки
import telebot
from database import *
from telebot import types
from time import sleep, localtime, strftime
import random


# Нужные данные
admin = '@AAnimeshnikk'
z_admin = '@pypcdev'
chat = 'https://t.me/twoxchat'
news = 'https://t.me/twoxnews'
id = '560083718' # Твой ид, что-бы бот кидал тебе вce, что происходит в боте

# Для киви апи
# token = ''         # https://qiwi.com/api
# phone = ''

# Апи бота, создаём переменную для управления ботом(отправки запросов на апи)
bot = telebot.TeleBot('1072358209:AAHiQ__0NsNCsQEbld73xv25zjr-zGWATds')

# Заставляем бота мониторить чат на наличие команды /start

NAME_CHANGED = True

@bot.message_handler(commands=['start'])
def reg(message):
    conn = NewConnectionToAccountsDatabase()
    try:
        data = conn.GetFullAccountDataByID(message.from_user.id)
        if data[TELEGRAM_NAME] == "@UnknownTelegramUser%s" % message.from_user.id and message.from_user.username is not None:
            conn.UpdateTelegramName(message.from_user.id, "@%s" % message.from_user.username)
    except:
        conn.CreateNewAccount(message.from_user.id)
        telegram_name = ""
        if message.from_user.username is not None:
            conn.UpdateTelegramName(message.from_user.id, "@%s"% message.from_user.username)
            telegram_name = "@%s"% message.from_user.username
        else:
            conn.UpdateTelegramName(message.from_user.id, "@UnknownTelegramUser%s" % message.from_user.id)
            telegram_name = "@UnknownTelegramUser%s" % message.from_user.id

        username = ""
        if message.from_user.first_name is not None and message.from_user.last_name is not None:
            username = message.from_user.first_name + " " + message.from_user.last_name
        elif message.from_user.first_name is not None:
            username = message.from_user.first_name
        else:
            username = message.from_user.last_name

        conn.UpdateUserName(message.from_user.id, username)

        bot.send_message(message.from_user.id, "✅ Вас успешно зарегестрировано. Текущий видемый никнейм: %s" % telegram_name)



    conn.CommitToDatabase()
    conn.CloseConnection()
    del conn

    main(message)

# Главное меню
def main(message):
    # Добавляем клавиатуру и кнопки
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='🐶 Аккаунт', callback_data='account')
    btn2 = types.InlineKeyboardButton(text = '💵 Деньги', callback_data = 'money')
    btn3 = types.InlineKeyboardButton(text = '🚑 Помощь', callback_data = 'help')
    btn4 = types.InlineKeyboardButton(text = '🏙 Комнаты(Фиксированые)', callback_data = 'roomsfix')
    btn5 = types.InlineKeyboardButton(text = '🌆 Комнаты(Динамические)', callback_data = 'roomsunfix')
    markup.row(btn1, btn2)
    markup.row(btn4)
    markup.row(btn5)
    markup.row(btn3)

    # Отправляем сообщение с кнопками
    bot.send_message(message.from_user.id,
    f'''
    ⭕️ Главное меню :

    👮‍♂️ Администратор : {admin}
    👮‍♂️ Зам. Администратора : {z_admin}

    💬 Чат : {chat}
    👁 Новости : {news}

    Нажмите \"🚑 Помощь\" для отображения инструкции.
    Приятой игры!
    ''',
        disable_web_page_preview = True,
        reply_markup = markup
        )

# Запускаем обработку кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    # Обработка кнопки "Помощь"
    if call.data == 'help':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='🐶 Аккаунт', callback_data='account')
        btn2 = types.InlineKeyboardButton(text='💵 Деньги', callback_data='money')
        btn3 = types.InlineKeyboardButton(text='🚑 Помощь', callback_data='help')
        btn4 = types.InlineKeyboardButton(text='🏙 Комнаты (Фиксированые)', callback_data='roomsfix')
        btn5 = types.InlineKeyboardButton(text='🌆 Комнаты (Динамические)', callback_data='roomsunfix')
        markup.row(btn1, btn2)
        markup.row(btn4)
        markup.row(btn5)
        markup.row(btn3)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text =
'''
Что бы играть:
Внесите на свой баланс депозит.
Выберите комнату под свою сумму либо зайдите в динамическую комнату.
(Динамическая комната - комната без фиксированой суммы для игры но с минимальной и максимальной ставкой.
В зависимости от суммы ставки будут изменятся и ваши шансы. Больше ставка - больше шанс)
Зайдя в комнату с фиксированой ставкой с вашего акаунта автоматически снимется сумма ставки.
В комнате с фиксированой ставкой шансы розделяются между игроками поровну.
В комнате с динамической ставкой вы будете должны ввести сумму ставки самостоятельно.
Как только в комнате будет больше трёх человек запускается таймер в 2 минуты.
За 5 секунд до конца таймера комната закрывается(пользователи не смогут больше подключатся)
По истечению таймера бот определяет победителя в зависимости от ваших шансов.
Победившему на акаунт перечесляется весь банк комнаты за исключением комисии бота - 10%.
Ввод и вывод денег осуществляется в меню "Деньги💵".


❗️❗️❗️

🔺🔺🔺КОМИССИЯ МОЖЕТ БЫТЬ УМЕНЬШЕНА ЕСЛИ У ПОБЕДИТЕЛЯ В ИМЕНИ ЕСТЬ "@twoxmoney_bot"🔺🔺🔺
При наличии у победившего пользователя в имени или в фамилии аккаунта телеграм строки "@twoxmoney_bot" комиссия для этого пользователя уменьшается до 5%
''',
        reply_markup = markup)

    # Переход в главное меню
    elif call.data == 'menu':

        # Повторяем всё из функции main()
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='🐶 Аккаунт', callback_data='account')
        btn2 = types.InlineKeyboardButton(text = '💵 Деньги', callback_data = 'money')
        btn3 = types.InlineKeyboardButton(text = '🚑 Помощь', callback_data = 'help')
        btn4 = types.InlineKeyboardButton(text = '🏙 Комнаты (Фиксированые)', callback_data = 'roomsfix')
        btn5 = types.InlineKeyboardButton(text = '🌆 Комнаты (Динамические)', callback_data = 'roomsunfix')
        markup.row(btn1, btn2)
        markup.row(btn4)
        markup.row(btn5)
        markup.row(btn3)

        # Редактируем сообщение с кнопками
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text =
f'''
⭕️ Главное меню :

👮‍♂️ Администратор : {admin}
👮‍♂️ Зам. Администратора : {z_admin}
💬Чат : {chat}
👁Новости : {news}

Нажмите \"Помощь🚑\" для отображения инструкции.
Приятой игры!
''',
        disable_web_page_preview = True,
        reply_markup = markup
        )

    # Переход в "Деньги"
    elif call.data == 'money':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text = '🏦 Ввод', callback_data = 'deposit')
        btn1 = types.InlineKeyboardButton(text = '💸 Вывод', callback_data = 'withdrawal')
        back = types.InlineKeyboardButton(text = '🔙 Назад', callback_data = 'menu')
        markup.row(btn)
        markup.row(btn1)
        markup.row(back)
        bot.edit_message_text(chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        text ='Выберите что хотите сделать : ',
        reply_markup = markup)

    # Депозит
    elif call.data == 'deposit':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text = '15 руб', callback_data = '15r')
        btn1 = types.InlineKeyboardButton(text = '30 руб', callback_data = '30r')
        btn2 = types.InlineKeyboardButton(text = '50 руб', callback_data = '50r')
        btn3 = types.InlineKeyboardButton(text = '100 руб', callback_data = '100r')
        btn4 = types.InlineKeyboardButton(text = '250 руб', callback_data = '250r')
        btn5 = types.InlineKeyboardButton(text = '500 руб', callback_data = '500r')
        btn6 = types.InlineKeyboardButton(text = '1000 руб', callback_data = '1000r')
        btn7 = types.InlineKeyboardButton(text = '2500 руб', callback_data = '2500r')
        btn8 = types.InlineKeyboardButton(text = '5000 руб', callback_data = '5000r')
        btn9 = types.InlineKeyboardButton(text = '10000 руб', callback_data = '10000r')
        back = types.InlineKeyboardButton(text = '🔙 Назад', callback_data = 'money')
        markup.row(btn,btn1)
        markup.row(btn2,btn3)
        markup.row(btn4, btn5)
        markup.row(btn6,btn7)
        markup.row(btn8,btn9)
        markup.row(back)

        bot.edit_message_text(chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        text ='Выберите сумму для пополнения баланса : ',
        reply_markup = markup)

    # Аккаунт
    elif call.data == "account":
        global NAME_CHANGED
        NAME_CHANGED = False
        conn = NewConnectionToAccountsDatabase()

        data = conn.GetFullAccountDataByID(call.message.chat.id)
        show_name = ""
        if data[PRIMARY_NAME] == TELEGRAM_NAME:
            show_name = data[TELEGRAM_NAME]
        else:
            show_name = data[USER_NAME]

        markup = types.InlineKeyboardMarkup()
        if data[PRIMARY_NAME] == TELEGRAM_NAME:
            btn1 = types.InlineKeyboardButton("Включить показ 2xM0NEY Username", callback_data="turn_user_name")
        else:
            btn1 = types.InlineKeyboardButton("Включить показ Telegram Nickname", callback_data="turn_telegram_name")
        btn2 = types.InlineKeyboardButton("Изменить 2xM0NEY Username", callback_data="change_user_name")
        back = types.InlineKeyboardButton(text = '🔙 Назад', callback_data = 'menu')
        markup.row(btn1)
        markup.row(btn2)
        markup.row(back)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
        text=f'''
👁‍🗨 Видимый никнейм: {show_name}

💰 Текущий баланс: {data[BALANCE]} руб.

🕒 Дата регистрации: {data[REGISTRATION_DATE]}

            ''', reply_markup=markup)

        conn.CloseConnection()
        del conn

    elif call.data == "turn_user_name":
        conn = NewConnectionToAccountsDatabase()
        showed_name = conn.GetFullAccountDataByID(call.message.chat.id)[USER_NAME]
        conn.UpdatePrimaryName(call.message.chat.id, USER_NAME)
        conn.CommitToDatabase()
        conn.CloseConnection()
        del conn

        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='🔙 Назад', callback_data='account')
        markup.row(back)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
        text='✅ Успешно! Теперь видимый никнейм: %s' % showed_name, reply_markup=markup)


    elif call.data == "turn_telegram_name":
        conn = NewConnectionToAccountsDatabase()
        showed_name = conn.GetFullAccountDataByID(call.message.chat.id)[TELEGRAM_NAME]
        conn.UpdatePrimaryName(call.message.chat.id, TELEGRAM_NAME)
        conn.CommitToDatabase()
        conn.CloseConnection()
        del conn

        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='🔙 Назад', callback_data='account')
        markup.row(back)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
        text='✅ Успешно! Теперь видимый никнейм: %s' % showed_name, reply_markup=markup)


    elif call.data == "change_user_name":
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='🔙 Назад', callback_data='account')
        markup.row(back)
        bot.send_message(call.message.chat.id, "⌨️ Введите новое имя")



        @bot.message_handler(func=lambda message: True, content_types=['text'])
        def change_name(message):
            global NAME_CHANGED
            if not NAME_CHANGED:
                if len(message.text) > 32:
                    bot.send_message(message.chat.id, "❌ Думаю тебе и 32 символов хватит с головой для оригинального никнейма!. \n⌨️ Введите новое имя")
                else:
                    bot.send_message(message.chat.id, "🌐 Проверка на оригинальность...")
                    conn = NewConnectionToAccountsDatabase()
                    data = conn.GetFullAccountDataByID(message.chat.id)
                    try:
                        dt = conn.GetFullAccountDataByUserName(message.text)
                        if dt[ID] == message.chat.id:
                            bot.send_message(message.chat.id, "❌ Зачем менять свое имя на тоже самое? \n⌨️ Введите новое имя",
                                             disable_web_page_preview=True)
                        else:
                            bot.send_message(message.chat.id, "❌ Такой уже есть, думаю тебе лучше иметь оригинальний никнейм, не так ли? \n⌨️ Введите новое имя")
                    except:
                        conn.UpdateUserName(message.chat.id, message.text)
                        msg = bot.send_message(message.chat.id, "✅ Отличний оригинальний никнейм! Никнейм изменен!",
                                          reply_markup=markup)
                        bot.register_next_step_handler(message, lambda x: x)
                        NAME_CHANGED = True
                    conn.CommitToDatabase()
                    conn.CloseConnection()
                    del conn

    elif call.data == 'roomsfix':
        conn = NewConnectionToFixedRoomsDatabase()
        onlines = conn.GetAllFixedRoomsOnline()
        conn.CloseConnection()
        del conn

        t = localtime()
        current_time = strftime("%H:%M:%S", t)

        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text=f'[{onlines["1"]}/10] 15 руб №1', callback_data='join_roomfix1')
        btn1 = types.InlineKeyboardButton(text=f'[{onlines["2"]}/10] 15 руб №2', callback_data = 'join_roomfix2')
        btn2 = types.InlineKeyboardButton(text=f'[{onlines["3"]}/10] 30 руб №3', callback_data = 'join_roomfix3')
        btn3 = types.InlineKeyboardButton(text=f'[{onlines["4"]}/10] 50 руб №4', callback_data = 'join_roomfix4')
        btn4 = types.InlineKeyboardButton(text=f'[{onlines["5"]}/10] 100 руб №5', callback_data = 'join_roomfix5')
        btn5 = types.InlineKeyboardButton(text=f'[{onlines["6"]}/10] 250 руб №6', callback_data = 'join_roomfix6')
        btn6 = types.InlineKeyboardButton(text=f'[{onlines["7"]}/10] 500 руб №7', callback_data = 'join_roomfix7')
        btn7 = types.InlineKeyboardButton(text=f'[{onlines["8"]}/10] 1000 руб №8', callback_data = 'join_roomfix8')
        btn8 = types.InlineKeyboardButton(text=f'[{onlines["9"]}/10] 2500 руб №9', callback_data = 'join_roomfix9')
        btn9 = types.InlineKeyboardButton(text=f'[{onlines["10"]}/10] 5000 руб №10', callback_data = 'join_roomfix10')
        btn10 = types.InlineKeyboardButton(text=f"🔄️ Обновить (последнее обновление {current_time})", callback_data="roomsfix")
        back = types.InlineKeyboardButton(text = '🔙 Назад', callback_data = 'menu')

        markup.row(btn,btn1)
        markup.row(btn2,btn3)
        markup.row(btn4, btn5)
        markup.row(btn6,btn7)
        markup.row(btn8,btn9)
        markup.row(btn10)
        markup.row(back)

        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,
        text = 'Выберите комнату', reply_markup = markup)

    elif "join_roomfix" in call.data:
        conn = NewConnectionToFixedRoomsDatabase()
        onlines = conn.GetAllFixedRoomsOnline()
        join_room_id = int(call.data[12:])
        data = conn.GetAllFixedRoomData(join_room_id)

        if onlines[str(join_room_id)] == data[MAX_ONLINE]:
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton(text = '🔙 Назад', callback_data = 'roomsfix')
            markup.row(back)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='❌ Комната заполненая, виберете другую!', reply_markup=markup)
        else:
            conn.AddNewUserToRoom(join_room_id, call.message.chat.id)
            conn.IncrementRoomCurrentOnline(join_room_id)
            conn.CommitToDatabase()
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(chat_id=call.message.chat.id, text=f"Вы присоединились к комнате с фиксированной ставкой - {data[CASH_SUM]}руб. Игра начинается при онлайне в 3 человека, когда начинает идти таймер на 2 минуты. Через две минуты будет выбран один победитель - который получит 95% общего банка (5% админам на мивинку). То есть баланс этого игрока будет увеличен на 95% от общего банка.")
            conn.CloseConnection()
            del conn

            current_online = 0
            while True:
                conn = NewConnectionToFixedRoomsDatabase()
                online = conn.GetAllFixedRoomsOnline()[str(join_room_id)]
                data = conn.GetAllFixedRoomData(join_room_id)
                max_online = data[MAX_ONLINE]
                if current_online != online:
                    acc_conn = NewConnectionToAccountsDatabase()
                    acc_data = acc_conn.GetFullAccountDataByID(conn.GetAllUsersFromRoom(join_room_id)[-1])
                    if acc_data[PRIMARY_NAME] == TELEGRAM_NAME:
                        name = acc_data[TELEGRAM_NAME]
                    else:
                        name = acc_data[USER_NAME]
                    current_online = online
                    bot.send_message(chat_id = call.message.chat.id,
                                            text=f"Присоединился игрок {name}. Текущий онлайн: {current_online}/{max_online}")
                if online >= 1:
                    break
                conn.CloseConnection()
                del conn
                sleep(1)


        conn = NewConnectionToFixedRoomsDatabase()
        conn.ClearUsersFromRoom(join_room_id)
        conn.UpdateRoomCurrentOnline(join_room_id, 0)
        conn.CommitToDatabase()
        conn.CloseConnection()
        del conn

    # Динамические комнаты
    elif call.data == 'roomsunfix':
        markup = types.InlineKeyboardMarkup()
        btn = btn = types.InlineKeyboardButton(text = f'''[0/10] 15-50 руб №1''', callback_data = 'roomunfix1')
        btn1 = types.InlineKeyboardButton(text = f'''[0/10] 15-50 руб №2''', callback_data = 'roomunfix2')
        btn2 = types.InlineKeyboardButton(text = f'''[0/10] 30-80 руб №3''', callback_data = 'roomunfix3')
        btn3 = types.InlineKeyboardButton(text = f'''[0/10] 50-100 руб №4''', callback_data = 'roomunfix4')
        btn4 = types.InlineKeyboardButton(text = f'''[0/10] 100 руб №5''', callback_data = 'roomunfix5')
        btn5 = types.InlineKeyboardButton(text = f'''[0/10] 250 руб №6''', callback_data = 'roomunfix6')
        btn6 = types.InlineKeyboardButton(text = f'''[0/10] 500 руб №7''', callback_data = 'roomunfix7')
        btn7 = types.InlineKeyboardButton(text = f'''[0/10] 1000 руб №8''', callback_data = 'roomunfix8')
        btn8 = types.InlineKeyboardButton(text = f'''[0/10] 2500 руб №9''', callback_data = 'roomunfix9')
        btn9 = types.InlineKeyboardButton(text = f'''[0/10] 5000 руб №10''', callback_data = 'roomunfix10')

        back = types.InlineKeyboardButton(text = '🔙 Назад', callback_data = 'menu')

        markup.row(btn,btn1)
        markup.row(btn2,btn3)
        markup.row(btn4, btn5)
        markup.row(btn6,btn7)
        markup.row(btn8,btn9)
        markup.row(back)

        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,
        text = 'Выберите комнату :', reply_markup = markup)

# Включаем цикл для бота
bot.polling(none_stop=True)
