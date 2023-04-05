

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


#https://api.openweathermap.org/data/2.5/weather?q=London,uk&appid={c1187b3eaa7f19a879772ca85bc06244}&lang=ru&units=metric


class WeatherApi:
    def __init__(self, token):
        self.tooken = token



class Bot:
    def __init__(self, token):
        print("Загрузка...")
        self.token = token
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.weather_api = WeatherApi('c1187b3eaa7f19a879772ca85bc06244')
        self.add_handlers()

    def work(self):
        self.updater.start_polling()
        print("Бот готов к работе!")
        self.updater.idle()


    def enable_logging(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                             level=logging.INFO)


    def add_handlers(self):
        start_handler = CommandHandler('start', self.start) # /start
        self.dispatcher.add_handler(start_handler)

        msg_handler = MessageHandler(Filters.text & (~Filters.command), self.msg)
        self.dispatcher.add_handler(msg_handler)

        weather_handler = CommandHandler('weather', self.show_weather) # /weather
        self.dispatcher.add_handler(weather_handler)

        unknown_handler = MessageHandler(Filters.command, self.unknown)
        self.dispatcher.add_handler(unknown_handler)

    def show_weather(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                  text="")

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                  text="Привет, я бот")

    def msg(self, update, context):
        if update.message.text.lower() == 'привет':
            text = 'Привет :)'
        else:
            text = f"Я получил сообщение {update.message.text}. Даже не знаю что вам ответить"
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    def unknown(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Не известные мне команды")

bot = Bot('6043462615:AAE9xDEwnJY_erj-A1wE4QL2BwYulvDIAYI')
bot.work()