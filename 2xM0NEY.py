# Импортируем нужные библиотеки
import telebot
from telebot import types
from SimpleQIWI import *
from time import sleep
import sqlite3
import Token

# Нужные данные
admin = Token.admin
chat = 'https://t.me/twoxchat'
news = 'https://t.me/twoxnews'
id = Token.id # Твой ид, что-бы бот кидал тебе все, что происходит в боте

# Для киви апи
token = Token.QIVY         # https://qiwi.com/api
phone = Token.phone

# Апи бота, создаём переменную для управления ботом(отправки запросов на апи)
bot = telebot.TeleBot(Token.TOKEN)

# Создаём переменную для id
chat_id = ''

# Заставляем бота мониторить чат на наличие команды /start
@bot.message_handler(commands=['start'])
def main(message):
    chat_id = message.from_user.id # Узнаём айди юзера и записываем в переменную
    bot.delete_message(message.from_user.id, message.message_id) # Удаляем сообщение с командой /start

    # Добавляем клавиатуру и кнопки
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text = 'Аккаунт🐶', callback_data = 'accaunt')
    btn2 = types.InlineKeyboardButton(text = 'Деньги💵', callback_data = 'money')
    btn3 = types.InlineKeyboardButton(text = 'Помощь🚑', callback_data = 'help')
    btn4 = types.InlineKeyboardButton(text = 'Комнаты🏙\n(Фиксированые)', callback_data = 'rooms')
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

    conn = sqlite3.connect('2xM0NEY.db')
    cursor = conn.cursor()
    print('Запись')
    cursor.execute(
    '''CREATE TABLE IF NOT EXISTS users
    (id INTEGER, name VARCHAR, link VARCHAR)''')
    print('Записано...')
    conn.commit()
    conn.close()
    print('закрыто')

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

    # Возврат в меню

    # Возврат в главное меню
    elif call.data == 'menu':
        # Повторяем всё из функции main()
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text = 'Аккаунт🐶', callback_data = 'accaunt')
        btn2 = types.InlineKeyboardButton(text = 'Деньги💵', callback_data = 'money')
        btn3 = types.InlineKeyboardButton(text = 'Помощь🚑', callback_data = 'help')
        btn4 = types.InlineKeyboardButton(text = 'Комнаты🏙\n(Фиксированые)', callback_data = 'rooms')
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
        try:
            api = QApi(token=token, phone=phone)
            api.stop()    # Отключаем приём платежей если они включены
        except:
            bot.send_message(id, "ОШИБКА С КИВИ АПИ")

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

    # 15 руб
    elif call.data == '15r':
        message = call.message
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text = 'Назад🔙', callback_data = 'deposit')
        markup.add(btn)

        api = QApi(token=token, phone=phone)

        price = 15                  # Минимальное значение при котором счет будет считаться закрытым
        comment = api.bill(price)   # Создаем счет. Комментарий с которым должен быть платеж генерируется автоматически, но его можно задать                                 # параметром comment. Валютой по умолчанию считаются рубли, но ее можно изменить параметром currency

        bot.send_message(id, str(message.chat.first_name) + " [ "+ str(message.chat.id)+f" ] | Оплачивает {price} руб")

        bot.edit_message_text(chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        text = "Переведите %i рублей на счет %s с комментарием '%s' (только без кавычек)" % (price, phone, comment),
        reply_markup = markup)

        try:
            api.start()                 # Начинаем прием платежей
        except:
            bot.send_message(id, "ОШИБКА С КИВИ АПИ")
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text = 'Назад🔙', callback_data = 'deposit')
            markup.add(btn)
            bot.edit_message_text(chat_id = call.message.chat.id,
            message_id = call.message.message_id,
            text = "Простите, но произошла ошибка с qiwi api, бот уже сообщил администратору :3\nПопробуйте пожалуйста позже...",
            reply_markup = markup)

        while True:
            if api.check(comment):  # Проверяем статус
                bot.answer_callback_query(callback_query_id=cmd.id, text="Платёж успешно получен!\nМожете тажимать \"Продолжить🔙\"", show_alert=True)
                markup = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton(text = 'Продолжить🔙', callback_data = 'deposit')
                markup.add(btn)
                bot.edit_message_text(chat_id = call.message.chat.id,
                message_id = call.message.message_id,
                text = "Готово! Деньги на вашем счёте!",
                reply_markup = markup)
                bot.send_message(id, str(message.chat.first_name) + " [ "+ str(message.chat.id)+f" ] | Оплатил {price} руб")
                break

            sleep(1)

        api.stop()                  # Останавливаем прием платежей

# Включаем цикл для бота
bot.polling(none_stop = True)
