from __future__ import annotations
from random import randint
import telebot
import json
from telebot import types
import requests
from telebot.handler_backends import StatesGroup, State

'''
@FilmFans_bot это бот для поиска фильмов/сериалов/аниме/мультсериалов/мультфильмов по жанрам комедия/мелодрама/драма/криминал/ужасы
'''

info = {}
class User:
    def __init__(self):
        self.name_user = None
        self.choice = {
            "movie": 0,
            "tv-series": 0,
            "cartoon": 0,
            "animated-series": 0,
            "anime": 0
        }
    
    def userInfo(self):
        info["name"] = self.name_user
        info["often_choice"] = max(self.choice, key=self.choice.get)
        info["cnt"] = self.choice[info["often_choice"]]
        with open(f'users\\{self.name_user}.json', 'w') as file:
            json.dump(info, file)



class Bot(User):
    def __init__(self):
        super().__init__()
        self.bot = telebot.TeleBot('8060981054:AAHr4ABCYxfZh4v9CVj0Ik9b72CWW9B-PT8')
        self.API = 'VBY5519-WKA4BJJ-J03MDYZ-ZRPRBV7'
        media_type = None
        genre_media = None

        @self.bot.message_handler(commands=['start'])
        def main(message):
            self.bot.send_message(message.chat.id, f'Приветствую тебя, маленький кинолюбитель! \n{message.from_user.first_name}, приготовься, ведь скоро тебя ждёт увлекательный просмотр фильмов, сериалов и прочего! Введи команду /search для поиска. Для справки, в моём боты вы можете найти "Фильм", "Сериал", "Аниме", "Мультфильм" или "Мультсериал". Для начала поиска можно ввести с клавитуры, главное, чтобы сообщение содержало такое же слово, как написано выше)')
            self.name_user = message.from_user.username

        @self.bot.message_handler(commands=['help'])
        def main(message):
            self.bot.send_message(
                message.chat.id, 'Help information'
            )


        @self.bot.message_handler(commands=['search'])
        def info(message):
            chat_id = message.chat.id
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup1 = telebot.types.KeyboardButton(text='Фильм')
            markup2 = telebot.types.KeyboardButton(text='Сериал')
            markup3 = telebot.types.KeyboardButton(text='Мультфильм')
            markup4 = telebot.types.KeyboardButton(text='Мультсериал')
            markup5 = telebot.types.KeyboardButton(text='Аниме')
            keyboard.add (markup1, markup2)
            keyboard.add (markup3, markup4, markup5)
            self.bot.send_message(chat_id, 'Что ты хочешь посмотреть?', reply_markup=keyboard)
            

        @self.bot.message_handler(func=lambda message: message.text in ['Фильм', 'Сериал', 'Мультфильм', 'Мультсериал', 'Аниме'])   
        def get_search_type(message):
            global media_type
            if message.text.lower() == 'аниме':
                self.bot.send_message(message.chat.id, f'{message.from_user.first_name}, выбери жанр аниме /genres, которые тебе нравятся, и я найду что-нибудь для тебя). Опять же можно ввести с клавитуры "Драма", "Комедия", "Мелодрама", "Криминал" или "Ужасы"', reply_markup=types.ReplyKeyboardRemove())
                media_type = 'anime'
            else:
                self.bot.send_message(message.chat.id, f'{message.from_user.first_name}, выбери жанр {message.text.lower()}ов /genres, которые тебе нравятся, и я найду что-нибудь для тебя). Опять же можно ввести с клавитуры "Драма", "Комедия", "Мелодрама", "Криминал" или "Ужасы"', reply_markup=types.ReplyKeyboardRemove())
                
                if message.text.lower() == 'фильм':
                    media_type = 'movie'
                elif message.text.lower() == 'сериал':
                    media_type = 'tv-series'
                elif message.text.lower() == 'мультфильм':
                    media_type = 'cartoon'
                elif message.text.lower() == 'мультсериал':
                    media_type = 'animated-series'
            self.choice[media_type] += 1

        @self.bot.message_handler(commands=['genres'])
        def info(message):
            chat_id = message.chat.id
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            mark1 = telebot.types.KeyboardButton(text='Драма')
            mark2 = telebot.types.KeyboardButton(text='Мелодрама')
            mark3 = telebot.types.KeyboardButton(text='Криминал')
            mark4 = telebot.types.KeyboardButton(text='Ужасы')
            mark5 = telebot.types.KeyboardButton(text='Комедия')
            keyboard.add (mark1, mark2)
            keyboard.add (mark3, mark4, mark5)
            self.bot.send_message(chat_id, 'Перед тобой каталог жанров:', reply_markup=keyboard)

        @self.bot.message_handler(func=lambda message: message.text in ['Драма', 'Мелодрама', 'Криминал', 'Ужасы', 'Комедия'])
        def get_search_genres(message):
            lasted_films = [] # сохраняем названия фильмов, которые нам предложил бот
            count_err = 0   # когда счётчик дойдёт до 15 работа закончится
            def get_movies_by_genres(media, genre, count_err):
                headers = {"X-API-KEY": self.API}
                params = {
                    'page': randint(1, 15),
                    'type': media,
                    'selectFields': ['name', 'year', 'countries', 'genres', 'description', 'rating', 'poster'],
                    'notNullFields': ['name', 'description', 'rating.kp', 'poster.url'],
                    'genres.name': f'+{genre.lower()}',
                    'sortField': 'rating.kp',
                    'sortType': '-1'
                }
                response = requests.get(
                    'https://api.kinopoisk.dev/v1.4/movie',
                    headers=headers,
                    params=params
                )
                data = response.json()
                if data['docs']:
                    film = data['docs'][0]
                    self.name = film.get('name')
                    description = film.get('description')
                    rating = film.get('rating', {}).get('kp', 'Не оценен')
                    poster = film.get('poster', {}).get('previewUrl' and 'url', (None, None))

                    if self.name not in lasted_films:
                        return f'{self.name}\n\n{description}\n\nРейтинг: {rating}\n\n{poster}'
                    elif count_err < 15:
                        count_err += 1
                        return new_media(count_err)
                    self.bot.send_message(message.chat.id, 'Фильмов больше не осталось по вашему запросу', reply_markup=types.ReplyKeyboardRemove())


            def new_media(count_err):
                global genre_media, media_type
                genre_media = message.text.lower()

                if not count_err:
                    self.bot.send_message(message.chat.id, f'Хорошо, сейчас что-нибудь подберу для тебя)')
                self.bot.send_message(message.chat.id, get_movies_by_genres(media_type, genre_media, count_err))
                lasted_films.append(self.name)
                chat_id = message.chat.id
                keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                mark1 = telebot.types.KeyboardButton(text=f'Переизбрать {media_type}')
                mark2 = telebot.types.KeyboardButton(text='Выбрал фильм из предложенного, пока)')
                keyboard.add (mark1, mark2)
                self.bot.send_message(chat_id, 'Хочешь найти что-нибудь другое?)', reply_markup=keyboard)

                @self.bot.message_handler(func=lambda message: message.text in [f'Переизбрать {media_type}', 'Выбрал фильм из предложенного, пока)'])
                def other_or_bye(message):
                    if message.text == 'Выбрал фильм из предложенного, пока)':
                        self.bot.send_message(message.chat.id, 'Приятного просмотра! Чтобы начать поиск заново выберите /start', reply_markup=types.ReplyKeyboardRemove())
                        self.userInfo()
                    else:
                        self.choice[media_type] += 1
                        count_err = 0
                        new_media(count_err)
            new_media(count_err)

    
    def run(self):
        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    bot = Bot()
    bot.run()