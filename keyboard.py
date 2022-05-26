from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

btn1=types.KeyboardButton('▲ Определить геолокацию', request_location = True)
btn2=types.KeyboardButton('🌯 Рейтинг шаурмичных')
btn3 = types.KeyboardButton('🧑 Личный кабинет')
btn4 = types.KeyboardButton('💬 Поддержка')
btn5 = types.KeyboardButton('🌯 Добавить шаурмичную')
btn6 = types.KeyboardButton('💬 Добавить отзыв')
btn7 = types.KeyboardButton('💬 Просмотр отзывов')

start.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)