# encoding: utf-8
# WeatherSnap bot
# Python 3.14


"""
This script implements the complete functionality 
for the WeatherSnap Telegram bot: 
https://t.me/Weather_Snap_Bot
"""


# imports

import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


# constants and objects

WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5/weather"
API_KEY: str = "API_KEY"
EMOJI_CODE: dict = {
                   }
TOKEN: str = "8627950136:AAEKai4ySidUVnQFX3yEkoyFB_6SszA8TZQ"
bot = telebot.Telebot(TOKEN)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Получить погоду", request_location=True))
keyboard.add(KeyboardButton("О проекте"))


# functionality

def get_weather(lat, lon) -> str:
    """Send request to OpenWeatherMap.org API
    at provided coordinates and return a message"""
    
    params: dict = {"let": lat,
                    "lon": lon,
                    "lang": "ru",
                    "units": "metric",
                    "appid": API_KEY}
    response = requests.get(url="WEATHER_API_URL, params=params).json()
    
    city_name = response["name"]
    description = response["weather"][0]["description"]
    code = response["weather"][0]["id"]
    temp = response["main"]["temp"]
    temp_feels_like = response["main"]["feels_like"]
    humidity = response["main"]["humidity"]
    emoji = EMOJI_CODE[code]
    
    message = f"Погода в: {city_name}\n"
    message += f"{emoji} {description.capitalize()}\n"
    message += f"Температура: {temp} C\n"
    message += f"Ощущается как {temp_feels_like}C\n"
    message += f"Влажность: {humidity}\n"
    
    return message


@bot.message_handler(commands=["start])
def send_welcome(message):
    """Send welcome message"""
    
    text: str = "Отправь мне своё местоположение "
    text += "и я отправлю тебе погоду."
    bot.send_message(message.chat.id,
                     text,
                     reply_keyboard=keyboard)


@bot.message_handler(content_types=["location"])
def send_weather(message):
    """Get weather data from the loaction provided 
    by the user and send the data"""
    
    lon = message.location.longitude
    lat = message.location.latitude
    result = get_weather(lat, lon)
    
    if result:
        bot.send_message(message.chat.id,
                         result,
                         reply_keyboard=keyboard)
    else:
        bot.send_message(message.chat.id,
                         "Что-то пошло не так",
                         reply_keyboard=keyboard)


@bot.message_handler(regexp="О проекте")
def send_project_info(message):
    """Send message about the project"""
    
    text: str = "What am I supposed to say about this"
    bot.send_message(message.chat.id,
                     text,
                     reply_keyboard=keyboard)


# start the bot
bot.infinity_polling()
