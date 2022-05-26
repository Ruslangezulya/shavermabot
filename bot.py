
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
        await bot.send_message(message.chat.id, text = "*Введите ваше обращение в данной форме: '/sup Обращение'*", parse_mode='Markdown')
    if message.text == "Оплатил":
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO premium (user_id, status) VALUES("{message.from_user.id}", "На рассмотрении")')
        conn.commit()
        await bot.send_message(message.chat.id, text = "*Оповещение администратору было отправлено. В скором времени он проверит оплату и выдаст вам Premium!*", parse_mode='Markdown') 
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()        
        cur.execute(f'SELECT * FROM premium WHERE status = "На рассмотрении"')
        result = cur.fetchall()
        str_out = ""
        for i in range(len(result)):
            date = result[i]
            str_out += f'\nНомер заявки: {date[0]}\n Айди пользователя: {date[1]}\n Имя пользователя: {message.from_user.first_name} \n'
        await bot.send_message(487142104, f'🌯Новая заявка на Premium. Проверьте оплату от пользователя.{str_out}\n Для выдачи премиума пользователю введите "/opl айди заявки"')
        
    if message.text == "😎 ШавермаБот Premium":
        id = message.chat.id
        await bot.send_message(message.chat.id, f'Вы собираетесь приобрести подписку ШавермаБот Premium!\nТолько до 01.07.2022г. ШавермаБот Premium НАВСЕГДА стоит всего 100 руб. \nРеквизиты для оплаты: \n Сбербанк - 4276522038191047 \n QIWI - +79524117050 \n Комментарий к платежу: {id}\nПосле оплаты напишите "Оплатил"')
    if message.text == "🌯 Рейтинг шаурмичных":
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()       
        conn.commit()       
        cur.execute(f'SELECT * FROM shawarma WHERE status = "Одобрено" ORDER BY rating DESC')
        result = cur.fetchall()
        str_out = ""
        for i in range(len(result)):
            date = result[i]       
            str_out += f'🌯{date[1]}. {date[3]}. Рейтинг: {date[6]}★ Внутренний номер: {date[7]}🌯 \n'
        print(str_out)
        await bot.send_message(message.chat.id, f'{str_out}')  
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
    if message.text == "🌯 Добавить шаурмичную":
        await bot.send_message(message.chat.id, text = "*Пришлите, пожалуйста геолокацию шаурмичной по кнопке 'Определить геолокацию'*", parse_mode='Markdown')
    if message.text == "💬 Добавить отзыв":
        await bot.send_message(message.chat.id, text = "*Отправьте, пожалуйста, ваш отзыв в данной форме: '/add Внутренний номер шаурмичной / Оценка (от 1 до 5 ★) / Текст отзыва' \nВнутренний номер смотрите в рейтинге шаурмичных.*", parse_mode='Markdown')
    if message.text == "💬 Просмотр отзывов":
        await bot.send_message(message.chat.id, text = "*Введите '/view Внутренний номер шаурмичной'\nВнутренний номер смотрите в рейтинге шаурмичных.*", parse_mode='Markdown')
    
        
        
    if "/new" in message.text:
        message_info = message.text[5:]
        if len(message_info) > 1:
            message_arr = message_info.split(" / ")
            name = message_arr[0]
            address = message_arr[1]            
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()      

            cur.execute(f'SELECT * FROM shawarma WHERE user_id = "{message.chat.id}" ORDER BY id DESC LIMIT 1')
            result = cur.fetchall()
            print(result)
            
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute(f'UPDATE shawarma SET name = "{name}", address = "{address}" WHERE id = "{result[0][0]}"')
            conn.commit()
            
            cur.execute(f'SELECT * FROM shawarma WHERE status = "На модерации"')
            result = cur.fetchall()
            str_out = ""
            for i in range(len(result)):
                date = result[i]
                str_out += f'{date[0]}. {date[1]}. {date[3]} \n'
            print(str_out)
            await bot.send_message(message.chat.id, text = "*Шаурмичная успешно отправлена на модерацию. При успешном одобрении администратором она появится в каталоге в течение 24 часов. *", parse_mode='Markdown')  
            await bot.send_message(487142104, f'🌯Новая заявка на добавление шаурмичной🌯 \n{str_out}Введите "/approve айди шаурмичной", чтобы одобрить шаурмичную')
            await bot.send_message(919654490, f'🌯Новая заявка на добавление шаурмичной🌯 \n{str_out}Введите "/approve айди шаурмичной", чтобы одобрить шаурмичную')                  
        else:
            await bot.send_message(message.chat.id, text = "*Вы не ввели данные о шаурмичной.*", parse_mode='Markdown')  
    if "/approve" in message.text:
        if message.chat.id == 487142104 or message.chat.id == 919654490:      
            message_info = message.text[9:]
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute(f'UPDATE shawarma SET status = "Одобрено" WHERE id = "{message_info}"')
            conn.commit()
            await bot.send_message(message.chat.id, f'🌯Шаурмичная успешно одобрена🌯')
        else: 
             await bot.send_message(message.chat.id, f'Вы не являетесь администратором.')
    if "/opl" in message.text:
        message_info = message.text[5:]
        if message.chat.id == 487142104 or message.chat.id == 919654490:                  
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute(f'UPDATE premium SET status = "Одобрено" WHERE id_zayavki = "{message_info}"')
            conn.commit()
            await bot.send_message(message.chat.id, f'🌯Премиум успешно выдан🌯')
        else: 
             await bot.send_message(message.chat.id, f'Вы не являетесь администратором.')
    if "/sup" in message.text:
        message_info = message.text[5:]
        if len(message_info) > 1:
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute(f'INSERT INTO support (user_name, appeal, sup_status) VALUES("@{message.from_user.username}", "{message_info}", "На рассмотрении")')
            conn.commit()           
            cur.execute(f'SELECT * FROM support WHERE sup_status = "На рассмотрении"')
            result = cur.fetchall()
            str_out = ""
            for i in range(len(result)):
                date = result[i]
                str_out += f'{date[0]}. {date[1]}. {date[2]} \n'
            print(str_out)
            await bot.send_message(message.chat.id, f'🧑 Ваше обращение успешно зарегистрировано. В течение 24 часов с вами свяжется администратор.')
            await bot.send_message(487142104, f'🧑 Новое обращение🧑 \n{str_out}\n Для того, чтобы пометить обращение, как рассмотренное, введите "/rev номер обращения"')
            await bot.send_message(919654490, f'🧑 Новое обращение🧑 \n{str_out}\n Для того, чтобы пометить обращение, как рассмотренное, введите "/rev номер обращения"')
        else:
            await bot.send_message(message.chat.id, f'🧑 Вы не ввели обращение.')
    if "/rev" in message.text:
        if message.chat.id == 487142104 or message.chat.id == 919654490:
            message_info = message.text[5:]
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute(f'UPDATE support SET sup_status = "Рассмотрено" WHERE sup_id = "{message_info}"')
            conn.commit()
            await bot.send_message(message.chat.id, f'🧑Обращение успешно помечено рассмотренным🧑')
        else:
            await bot.send_message(message.chat.id, f'🧑Вы не являетесь администратором.🧑')
        
    if "/add" in message.text:
        message_inform = message.text[5:]
        if len(message_inform)> 1: 
            message_arr = message_inform.split(" / ")
            vn_nom = message_arr[0]
            score = int(message_arr[1])
            review = message_arr[2]      
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM shawarma WHERE id = {vn_nom}')
            result = cur.fetchall()
            rate = result[0][6]
            rate_itog = (rate + score) / 2
            cur.execute(f'UPDATE shawarma SET rating = {rate_itog} WHERE id = {vn_nom}')
            cur.execute(f'INSERT INTO reviews (name, vn_nom, score, review, user_id) VALUES ("{message.from_user.first_name}", "{vn_nom}", "{score}", "{review}", "{message.chat.id}")')
            result = cur.fetchall()
            print(result)
            conn.commit()
            await bot.send_message(message.chat.id, text = "*Ваш отзыв успешно оставлен! Спасибо!*", parse_mode='Markdown')
        else:
            await bot.send_message(message.chat.id, text = "*Вы не ввели отзыв.*", parse_mode='Markdown')
    if "/view" in message.text:
        message_info = message.text[6:]
        if len(message_info) > 1:            
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()              
            cur.execute(f'SELECT * FROM reviews WHERE vn_nom = "{message_info}"')
            result = cur.fetchall()
            conn.commit()  
            str_out = ""
            for i in range(len(result)):
                date = result[i]
                str_out += f'Имя: {date[1]}. Оценка: {date[3]}★. Текст отзыва: {date[4]}.  \n'
            print(str_out)
            await bot.send_message(message.chat.id, f'{str_out}')
        else:
            await bot.send_message(message.chat.id, text = "*Вы не ввели параметры отзыва.*", parse_mode='Markdown')
        
         
 
@dp.message_handler(content_types=['location'])
async def get_message(message):
    print(message.location)
    latitude = message.location.latitude
    longitude = message.location.longitude
    
    coordinates = latitude, longitude
    
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()      

    cur.execute(f'SELECT * FROM users WHERE user_id = "{message.chat.id}" AND latitude > 0')
    result = cur.fetchall()
    
    if len(result) > 0:
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO shawarma (coordinates, status, user_id) VALUES ("{coordinates}", "На модерации", "{message.chat.id}")')
        conn.commit()
        await bot.send_message(message.chat.id, text = "* Введите '/new название шаурмичной / адрес шаурмичной', чтобы добавить информацию*", parse_mode='Markdown')  
    else:
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


