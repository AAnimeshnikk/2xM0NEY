# Импортируем нужные библиотеки
import telebot
from telebot import types
from time import sleep
import DB_account as acc
import random



# Нужные данные
admin = '@AAnimeshnikk'
chat = 'https://t.me/twoxchat'
news = 'https://t.me/twoxnews'
id = '560083718' # Твой ид, что-бы бот кидал тебе все, что происходит в боте

# Для киви апи
# token = ''         # https://qiwi.com/api
# phone = ''

# Апи бота, создаём переменную для управления ботом(отправки запросов на апи)
bot = telebot.TeleBot('1072358209:AAHiQ__0NsNCsQEbld73xv25zjr-zGWATds')

# Создаём переменную для id
chat_id = ''

# Заставляем бота мониторить чат на наличие команды /start
@bot.message_handler(commands=['start'])
def reg(message):
    global chat_id
    chat_id = message.from_user.id # Узнаём айди юзера и записываем в переменную
    acc_name = message.from_user.username

    def get_uname():
        @bot.message_handler(func=lambda message: True, content_types=['text'])
        def input_username(message):
            if len(message.text) < 30:
                acc.CreateNewAccount(message.from_user.id, 'Unknown' + str(chat_id))
                acc.SetAccountDataElement(message.from_user.id, "acc_username", 'Unknown' + str(chat_id))
                acc.SetAccountDataElement(message.from_user.id, "acc_showRealName", "False")
                acc.SetAccountDataElement(message.from_user.id, 'acc_username', message.text)
                main(message)
            else:
                bot.send_message(message.from_user.id, 'Слишком много символов, максимальное количество символов = 30 : ')
                get_uname()

    userindatabase = acc.AccountExistsByID(chat_id)

    if userindatabase == False and acc_name == None:
        bot.send_message(message.from_user.id, 'Введите желаемое имя пользователя (до 30 символов) : ')
        get_uname()

    elif userindatabase == False:
        acc.SetAccountDataElement(message.from_user.id, "acc_username", 'Unknown' + str(chat_id))
        acc_name = '@' + message.from_user.username
        acc.CreateNewAccount(message.from_user.id, acc_name)
        main(message)
    elif userindatabase == True:
        chat_id = message.from_user.id
        main(message)

def main(message):
    global chat_id
    # Добавляем клавиатуру и кнопки
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text = 'Аккаунт🐶', callback_data = 'accaunt')
    btn2 = types.InlineKeyboardButton(text = 'Деньги💵', callback_data = 'money')
    btn3 = types.InlineKeyboardButton(text = 'Помощь🚑', callback_data = 'help')
    btn4 = types.InlineKeyboardButton(text = 'Комнаты🏙\n(Фиксированые)', callback_data = 'roomsfix')
    btn5 = types.InlineKeyboardButton(text = 'Комнаты🌆\n(Динамические)', callback_data = 'roomsunfix')
    markup.row(btn1, btn2)
    markup.row(btn4, btn5)
    markup.row(btn3)

    # Отправляем сообщение с кнопками
    bot.send_message(chat_id,
    f'''
    ⭕️Главное меню :

    👮‍♂️Администратор : {admin}
    💬Чат : {chat}
    👁Новости : {news}

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
        btn1 = types.InlineKeyboardButton(text = 'Аккаунт🐶', callback_data = 'accaunt')
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
⭕️Главное меню:⭕️

👮‍♂️Администратор : {admin}
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
        btn2 = types.InlineKeyboardButton(text = 'Назад🔙', callback_data = 'menu')
        markup.row(btn)
        markup.row(btn1)
        markup.row(btn2)
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
    elif call.data == 'accaunt':
        show_realname = acc.GetAccountDataByID(call.message.chat.id)["acc_showRealName"]
        markup = types.InlineKeyboardMarkup()
        if show_realname == 'True':
            name_showed = call.from_user.username
            btn = types.InlineKeyboardButton(text = f'Выключить показ telegram nickname', callback_data = 'show_nicknamebtnoff')
        elif show_realname == 'False':
            name_showed = acc.GetAccountDataByID(call.message.chat.id)["acc_username"]
            btn = types.InlineKeyboardButton(text = f'Включить показ telegram nickname', callback_data = 'show_nicknamebtnon')

        back = types.InlineKeyboardButton(text = 'Назад🔙', callback_data = 'menu')
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id,
        text = f'Ваше имя : {name_showed}'

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
        btn = btn = types.InlineKeyboardButton(text = '[0:10] 15 руб №1', callback_data = 'roomunfix1')
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
