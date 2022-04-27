
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import config
import keyboard 
import logging 
import sqlite3
storage = MemoryStorage() 
bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
conn = sqlite3.connect('data.db')
cur = conn.cursor()
conn.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER, username TEXT, latitude FLOAT, longitude FLOAT)')
conn.commit();
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,)
  
                    

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, f"Шаверма-Бот приветствует вас, *{message.from_user.first_name}*! \nВоспользуйтесь меню ниже для выбора нужной опции.", reply_markup=keyboard.start, parse_mode='Markdown')
    try:
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users (user_id, username) VALUES("{message.from_user.id}", "@{message.from_user.username}")')
        conn.commit()
    except Exception as e:
        print(e)
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users (user_id) VALUES("{message.from_user.id}")')
        conn.commit()
       


 

    
@dp.message_handler(content_types=['text'])
async def get_message(message):
    
    if message.text == "💬 Поддержка":
        await bot.send_message(message.chat.id, text = "*Аналитик, тестировщик проекта Юлия - @vainnner* (по общим вопросам) * \nПрограммист, главный администратор проекта Руслан - @greycatrapper* (по техническим вопросам)", parse_mode='Markdown')
    if message.text == "🌯 Рейтинг шаурмичных":
        await bot.send_message(message.chat.id, text = "*К сожалению, пока что данная функция находится в разработке!*", parse_mode='Markdown')  
    if message.text == "🧑 Личный кабинет":
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()      

        cur.execute(f'SELECT * FROM users WHERE user_id = "{message.chat.id}"')
        result = cur.fetchall()
        print(result)
        
        if result[0][2] == None:
            geostr = ""
        else:
            geostr = f'🧑Ваша геолокация: {list(result[0])[2]}, {list(result[0])[3]}🧑'
        await bot.send_message(message.chat.id, f'🧑Ваше имя: {message.from_user.first_name}🧑\n🧑Ваш Telegram ID: {list(result[0])[0]}🧑\n{geostr}')
        
         
 
@dp.message_handler(content_types=['location'])
async def get_message(message):
    print(message.location)
    latitude = message.location.latitude
    longitude = message.location.longitude
    
    try:
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute(f'UPDATE users SET longitude = "{longitude}", latitude = "{latitude}" WHERE user_id = "{message.chat.id}"')
        conn.commit()
        await bot.send_message(message.chat.id, text = "*Ваша геолокация успешно добавлена в базу данных!*", parse_mode='Markdown') 
    except Exception as e:
        print(e)
    
    
   

if __name__ == '__main__':
    executor.start_polling(dp)


