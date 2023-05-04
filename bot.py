
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.parse
import urllib.request
import json

class WeatherApi:
    def __init__(self, token):
        self.token = token

    def data_for(self, *args):
        query = urllib.parse.quote_plus(','.join(args))
        url = f"https://api.openweathermap.org/data/2.5/weather?q={query}&appid={self.token}&lang=ru&units=metric"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode())
        return data


class Bot:
    def __init__(self, token):
        print("Загрузка...")
        self.token = token
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.weather_api = WeatherApi('')
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
        data = self.weather_api.data_for(*context.args)
        weather_data = f"{data['weather'][0]['description'].capitalize()}"
        temp_data = f"\nТемпература: {data['main']['temp']}. Ощущается как {data['main']['feels_like']}"
        wind_data = f"\nСкорость ветра: {data['wind']['speed']} м/с"
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text=f"{weather_data}{temp_data}{wind_data}")


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

bot = Bot('')
bot.work()
