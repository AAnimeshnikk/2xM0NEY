# Импортируем нужные библиотеки
import telebot
from telebot import types
from time import sleep
import DB_account as acc
import random

#---

# Нужные данные
admin = '@AAnimeshnikk'
z_admin = '@pypcdev'
chat = 'https://t.me/twoxchat'
news = 'https://t.me/twoxnews'
id = '560083718' # Твой ид, что-бы бот кидал тебе вce, что происходит в боте 123

# Для киви апи
# token = ''         # https://qiwi.com/api
# phone = ''

# Апи бота, создаём переменную для управления ботом(отправки запросов на апи)
bot = telebot.TeleBot('1072358209:AAHiQ__0NsNCsQEbld73xv25zjr-zGWATds')

# Заставляем бота мониторить чат на наличие команды /start
@bot.message_handler(commands=['start'])
def reg(message):
    userindatabase = acc.AccountExistsByID(message.from_user.id)

    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    if first_name is None:
        first_name = ""
    if last_name is None:
        last_name = ""

    if userindatabase == False and message.from_user.username == None:
        bot.send_message(message.from_user.id,
'''
У вас нету Telegram UserName, поэтому бот будет использовать ваши имя и фамилию.
Если среди учасников уже есть человек с такими именем и фамилией бот добавит в конец вашей фамилии ваш telegram id
''')
        showed_name = first_name + ' ' + last_name

        if acc.UsernameExists(showed_name) == True:
            unk = 'Unknown' + str(message.from_user.id)
            acc.CreateNewAccount(message.from_user.id, unk)
            if first_name == "" and last_name == "":
                showed_name = 'Unknown' + str(message.from_user.id)
            elif first_name == '':
                showed_name = last_name  + ' ' + str(message.from_user.id)
            else:
                showed_name = first_name + ' ' + last_name  + str(message.from_user.id)
            acc.SetAccountDataElement(message.from_user.id, 'acc_showRealName', 'False')
            acc.SetAccountDataElement(message.from_user.id, 'acc_username', showed_name)

        elif acc.UsernameExists(showed_name) == False:

            unk = 'Unknown' + str(message.from_user.id)
            acc.CreateNewAccount(message.from_user.id, unk)
            showed_name = first_name + ' ' + last_name
            acc.SetAccountDataElement(message.from_user.id, 'acc_showRealName', 'False')
            acc.SetAccountDataElement(message.from_user.id, 'acc_username', showed_name)

        if acc.GetAccountDataByID(message.from_user.id)['acc_showRealName'] == 'False':
            name = acc.GetAccountDataByID(message.from_user.id)["acc_username"]

        elif acc.GetAccountDataByID(message.from_user.id)['acc_showRealName'] == 'True':
            name = acc.GetAccountDataByID(message.from_user.id)["acc_name"]

        bot.send_message(message.from_user.id, f'Вы успешно зарегестрированы! \nВаш ник : {name}')
        main(message)


    elif userindatabase == False:
        acc.CreateNewAccount(message.from_user.id, message.from_user.username)
        acc.SetAccountDataElement(message.from_user.id, 'acc_showRealName', 'True')
        unk = 'Unknown' + str(message.from_user.id)
        acc.SetAccountDataElement(message.from_user.id, 'acc_username', unk)

        if acc.GetAccountDataByID(message.from_user.id)['acc_showRealName'] == 'False':
            name = acc.GetAccountDataByID(message.from_user.id)["acc_username"]

        elif acc.GetAccountDataByID(message.from_user.id)['acc_showRealName'] == 'True':
            name = acc.GetAccountDataByID(message.from_user.id)["acc_name"]

        bot.send_message(message.from_user.id, f'Вы успешно зарегестрированы! \nВаш ник : @{name}')

        main(message)

    elif userindatabase == True:

        if message.from_user.username != None:
                acc.SetAccountDataElement(message.from_user.id, 'acc_showRealName', 'True')
                acc.SetAccountDataElement(message.from_user.id, 'acc_name', message.from_user.username)

        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        if first_name is None:
            first_name = ""
        if last_name is None:
            last_name = ""

        if first_name == '':
            i = last_name
        else:
            i = first_name + ' ' + last_name

        if acc.UsernameExists(i) == True:
            if first_name == '':
                i = last_name + message.from_user.id
            elif first_name != '' and last_name != '':
                i = first_name + ' ' +last_name + ' ' + str(message.from_user.id)
            elif first_name != '' and last_name == '':
                i = first_name + ' ' + str(message.from_user.id)

        acc.SetAccountDataElement(message.from_user.id, 'acc_username', i)

        main(message)

# Главное меню
def main(message):
    # Добавляем клавиатуру и кнопки
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Аккаунт🐶', callback_data='accaunt_username')
    if acc.GetAccountDataByID(message.from_user.id)[acc.acc_showRealName] == "True":
        btn1 = types.InlineKeyboardButton(text='Аккаунт🐶', callback_data='accaunt_name')
    btn2 = types.InlineKeyboardButton(text = 'Деньги💵', callback_data = 'money')
    btn3 = types.InlineKeyboardButton(text = 'Помощь🚑', callback_data = 'help')
    btn4 = types.InlineKeyboardButton(text = 'Комнаты🏙\n(Фиксированые)', callback_data = 'roomsfix')
    btn5 = types.InlineKeyboardButton(text = 'Комнаты🌆\n(Динамические)', callback_data = 'roomsunfix')
    markup.row(btn1, btn2)
    markup.row(btn4, btn5)
    markup.row(btn3)

    # Отправляем сообщение с кнопками
    bot.send_message(message.from_user.id,
    f'''
    ⭕️ Главное меню :

    👮‍♂️ Администратор : {admin}
    👮‍♂️ Зам. Администратора : {z_admin}

    💬 Чат : {chat}
    👁 Новости : {news}

    Нажмите \"Помощь🚑\" для отображения инструкции.
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
        exit = types.InlineKeyboardButton(text = 'Закрыть', callback_data = 'menu')
        btn1 = types.InlineKeyboardButton(text='Связатся с администратором', url='https://t.me/AAnimeshnikk')
        btn2 = types.InlineKeyboardButton(text='Связатся с зам. администратором', url='https://t.me/pypcdev')
        markup.row(btn1)
        markup.row(btn2)
        markup.row(exit)
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
        btn1 = types.InlineKeyboardButton(text='Аккаунт🐶', callback_data='accaunt_username')
        if acc.GetAccountDataByID(call.message.chat.id)[acc.acc_showRealName] == "True":
            btn1 = types.InlineKeyboardButton(text = 'Аккаунт🐶', callback_data = 'accaunt_name')
        btn2 = types.InlineKeyboardButton(text = 'Деньги💵', callback_data = 'money')
        btn3 = types.InlineKeyboardButton(text = 'Помощь🚑', callback_data = 'help')
        btn4 = types.InlineKeyboardButton(text = 'Комнаты🏙\n(Фиксированые)', callback_data = 'roomsfix')
        btn5 = types.InlineKeyboardButton(text = 'Комнаты🌆\n(Динамические)', callback_data = 'roomsunfix')
        markup.row(btn1, btn2)
        markup.row(btn4, btn5)
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
        btn = types.InlineKeyboardButton(text = 'Ввод🏦', callback_data = 'deposit')
        btn1 = types.InlineKeyboardButton(text = 'Вывод💸', callback_data = 'withdrawal')
        back = types.InlineKeyboardButton(text = 'Назад🔙', callback_data = 'menu')
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
        back = types.InlineKeyboardButton(text = 'Назад🔙', callback_data = 'money')
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
    elif 'accaunt' in call.data:
        need_to_modify = True
        if call.data == "accaunt_name":
            if acc.GetAccountDataByID(call.message.chat.id)[acc.acc_name] == f"Unknown{call.message.chat.id}":
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='У вас нету Telegram Nickname!')
                need_to_modify = False
            else:
                if acc.GetAccountDataByID(call.message.chat.id)[acc.acc_showRealName] == "False":
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='Имя успешно изменено!')
                    acc.SetAccountDataElement(call.message.chat.id, acc.acc_showRealName, "True")
        else:
            if acc.GetAccountDataByID(call.message.chat.id)[acc.acc_showRealName] == "True":
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='Имя успешно изменено!')
            acc.SetAccountDataElement(call.message.chat.id, acc.acc_showRealName, "False")

        if need_to_modify:
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton(text='Назад🔙', callback_data='menu')
            if acc.GetAccountDataByID(call.message.chat.id)['acc_showRealName'] == 'True':
                accaunt_name = '@' + acc.GetAccountDataByID(call.message.chat.id)['acc_name']
                show_name = types.InlineKeyboardButton(text="Использовать Username", callback_data="accaunt_username")
            elif acc.GetAccountDataByID(call.message.chat.id)['acc_showRealName'] == 'False':
                accaunt_name = acc.GetAccountDataByID(call.message.chat.id)['acc_username']
                show_name = types.InlineKeyboardButton(text="Использовать Telegram Nickname",
                                                       callback_data="accaunt_name")
            markup.row(back)
            markup.row(show_name)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'''
👤 Ваше имя : {accaunt_name}

💰 Баланс : {acc.GetAccountDataByID(call.message.chat.id)['acc_balance']}
                    ''', reply_markup=markup)


    # Меню фиксированных комнат
    elif call.data == 'roomsfix':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text = '[0/10] 15 руб №1', callback_data = 'roomfix1')
        btn1 = types.InlineKeyboardButton(text = '[0/10] 15 руб №2', callback_data = 'roomfix2')
        btn2 = types.InlineKeyboardButton(text = '[0/10] 30 руб №3', callback_data = 'roomfix3')
        btn3 = types.InlineKeyboardButton(text = '[0/10] 50 руб №4', callback_data = 'roomfix4')
        btn4 = types.InlineKeyboardButton(text = '[0/10] 100 руб №5', callback_data = 'roomfix5')
        btn5 = types.InlineKeyboardButton(text = '[0/10] 250 руб №6', callback_data = 'roomfix6')
        btn6 = types.InlineKeyboardButton(text = '[0/10] 500 руб №7', callback_data = 'roomfix7')
        btn7 = types.InlineKeyboardButton(text = '[0/10] 1000 руб №8', callback_data = 'roomfix8')
        btn8 = types.InlineKeyboardButton(text = '[0/10] 2500 руб №9', callback_data = 'roomfix9')
        btn9 = types.InlineKeyboardButton(text = '[0/10] 5000 руб №10', callback_data = 'roomfix10')

        back = types.InlineKeyboardButton(text = 'Назад🔙', callback_data = 'menu')

        markup.row(btn,btn1)
        markup.row(btn2,btn3)
        markup.row(btn4, btn5)
        markup.row(btn6,btn7)
        markup.row(btn8,btn9)
        markup.row(back)

        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,
        text = 'Выберите комнату :', reply_markup = markup)

    # Динамические комнаты
    elif call.data == 'roomsunfix':
        markup = types.InlineKeyboardMarkup()
        btn = btn = types.InlineKeyboardButton(text = '[0/10] 15 руб №1', callback_data = 'roomunfix1')
        btn1 = types.InlineKeyboardButton(text = '[0/10] 15 руб №2', callback_data = 'roomunfix2')
        btn2 = types.InlineKeyboardButton(text = '[0/10] 30 руб №3', callback_data = 'roomunfix3')
        btn3 = types.InlineKeyboardButton(text = '[0/10] 50 руб №4', callback_data = 'roomunfix4')
        btn4 = types.InlineKeyboardButton(text = '[0/10] 100 руб №5', callback_data = 'roomunfix5')
        btn5 = types.InlineKeyboardButton(text = '[0/10] 250 руб №6', callback_data = 'roomunfix6')
        btn6 = types.InlineKeyboardButton(text = '[0/10] 500 руб №7', callback_data = 'roomunfix7')
        btn7 = types.InlineKeyboardButton(text = '[0/10] 1000 руб №8', callback_data = 'roomunfix8')
        btn8 = types.InlineKeyboardButton(text = '[0/10] 2500 руб №9', callback_data = 'roomunfix9')
        btn9 = types.InlineKeyboardButton(text = '[0/10] 5000 руб №10', callback_data = 'roomunfix10')

        back = types.InlineKeyboardButton(text = 'Назад🔙', callback_data = 'menu')

        markup.row(btn,btn1)
        markup.row(btn2,btn3)
        markup.row(btn4, btn5)
        markup.row(btn6,btn7)
        markup.row(btn8,btn9)
        markup.row(back)

        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,
        text = 'Выберите комнату :', reply_markup = markup)

# Включаем цикл для бота
bot.polling(none_stop = True)
