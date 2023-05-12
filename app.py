import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Здравствуйте! Меня зовут Бот-Конвертер валют!\nЧтобы начать работу введите команду в следующем формате:\n <имя валюты, цену которой вы хотите узнать> \
<имя валюты, в которой вы хотите узнать цену первой валюты> \
<количество первой валюты> \nЧтобы увидеть список всех доступных валют выберите команду: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в следующем формате:\n <имя валюты, цену которой вы хотите узнать> \
<имя валюты, в которой вы хотите узнать цену первой валюты> \
<количество первой валюты> \nЧтобы увидеть список всех доступных валют выберите команду: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) < 3:
            raise APIException('Слишком мало параметров.')
        if len(values) > 3:
            raise APIException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote}  - {(total_base*float(amount))} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
