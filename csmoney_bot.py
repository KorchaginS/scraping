import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from CS import collectData
import time

from bot_data import token

bot = Bot(token=token,parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['🔪Ножи','🥊Перчатики','🔫Снайперские винтовки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите категорию', reply_markup=keyboard)

@dp.message_handler(Text(equals='🔪Ножи'))
async def get_discount_knives(message: types.Message):
    await message.answer('Please wait...')

    collectData(cat_type=2)

    with open('CS_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    count = 0
    for  item in data:
        count += 1
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n'\
            f'{hbold("Скидка: ")}{item.get("discount")}%\n' \
            f'{hbold("Цена: ")}${item.get("item_price")}🔥'

        if count%20 ==0:
            time.sleep(3)

        if count == 100:
            break
        await message.answer(card)

@dp.message_handler(Text(equals='🔫Снайперские винтовки'))
async def get_discount_knives(message: types.Message):
    await message.answer('Please wait...')

    collectData(cat_type=4)

    with open('CS_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    count = 0
    for  item in data:
        count += 1
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n'\
            f'{hbold("Скидка: ")}{item.get("discount")}%\n' \
            f'{hbold("Цена: ")}${item.get("item_price")}🔥'

        if count%20 ==0:
            time.sleep(3)

        if count == 100:
            break
        await message.answer(card)

def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()