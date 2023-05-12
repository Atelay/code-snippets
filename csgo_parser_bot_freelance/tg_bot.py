import os
from time import sleep

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Text, Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand
from aiogram.utils.markdown import hbold, hlink

from parser_csgo import csgo_parser


load_dotenv()
bot = Bot(token=os.getenv("TOKEN"), parse_mode="HTML")
dp = Dispatcher()

current_discount = 10
min_price = 2_000
max_price = 10_000

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start', description='start bot'),
        BotCommand(command='/help', description='about bot and comand'),
        BotCommand(command='/discount', description='change discount'),
        BotCommand(command='/min', description='Change min price'),
        BotCommand(command='/max', description='Change max price')
        ]
    await bot.set_my_commands(main_menu_commands)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    button_1 = KeyboardButton(text='Ножи')
    button_2 = KeyboardButton(text='Перчатки')
    button_3 = KeyboardButton(text='Снайперские винтовки')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1, button_2, button_3]], 
                                   resize_keyboard=True, 
                                   one_time_keyboard=True)
    await message.answer(text='Выберите категорию для поиска', reply_markup=keyboard)


@dp.message(Command(commands=['help']))
async def process_start_command(message: Message):
    await message.answer(text=
                         'Привет. Я предназначен для поиска скинов CS:GO со скидкой. Вот список доступных команд:\n'
                         '/start - Начать поиск предметов.\n'
                         '/discount - Узнать либо изменить текущую скидку.\n'
                         '/min - Узнать либо изменить минимальный порог цены.\n'
                         '/max - Узнать либо изменить максимальный порог цены.\n', reply_markup=ReplyKeyboardRemove())


# Этот хэндлер будет срабатывать на ответ "Ножи" и удалять клавиатуру
@dp.message(Text(text='Ножи', ignore_case=True))
async def process_knives_answer(message: Message):
    data = await csgo_parser(category=2, discount=current_discount, min=min_price, max=max_price)
    for index, item in enumerate(data):
        card = f"{hlink(item.get('item_name'), item.get('item_3d'))}\n"\
               f"{hbold('Скидка: ')}{item.get('item_discount')}\n"\
               f"{hbold('Цена: ')}{item.get('item_price')}"
        if index%20 == 0: sleep(3)
        await message.answer(card, reply_markup=ReplyKeyboardRemove())


# Этот хэндлер будет срабатывать на ответ "Перчатки" и удалять клавиатуру
@dp.message(Text(text='Перчатки', ignore_case=True))
async def process_gloves_answer(message: Message):
    data = await csgo_parser(category=13, discount=current_discount, min=min_price, max=max_price)
    for index, item in enumerate(data):
        card = f"{hlink(item.get('item_name'), item.get('item_3d'))}\n"\
               f"{hbold('Скидка: ')}{item.get('item_discount')}\n"\
               f"{hbold('Цена: ')}{item.get('item_price')}"
        if index%20 == 0: sleep(3)
        await message.answer(card, reply_markup=ReplyKeyboardRemove())


# Этот хэндлер будет срабатывать на ответ "Снайперские винтовки" и удалять клавиатуру
@dp.message(Text(text='Снайперские винтовки', ignore_case=True))
async def process_guns_answer(message: Message):
    data = await csgo_parser(category=4, discount=current_discount, min=min_price, max=max_price)
    for index, item in enumerate(data):
        card = f"{hlink(item.get('item_name'), item.get('item_3d'))}\n"\
               f"{hbold('Скидка: ')}{item.get('item_discount')}\n"\
               f"{hbold('Цена: ')}{item.get('item_price')}"
        if index%20 == 0: sleep(3)
        await message.answer(card, reply_markup=ReplyKeyboardRemove())


# Этот хэндлер будет срабатывать на команду discount и предлогать изменить или показать текущую скидку
@dp.message(Command(commands=['discount']))
async def process_discount_command(message: Message):
    button_1 = KeyboardButton(text='Текущая скидка')
    button_2 = KeyboardButton(text='Изменить скидку')
    keyboard2 = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]], 
                                    resize_keyboard=True, 
                                    one_time_keyboard=True)
    await message.answer('Выберите действие:', reply_markup=keyboard2)


# Этот хэндлер будет срабатывать на текст 'Текущая скидка' и показывать текущую скидку
@dp.message(Text(text='Текущая скидка', ignore_case=True))
async def show_current_discount(message: Message):
    await message.answer(f'Текущая скидка: {current_discount}%', reply_markup=ReplyKeyboardRemove())


# Этот хэндлер будет срабатывать на текст 'Изменить скидку' и предлогать выбрать новое значение из предложенных
@dp.message(Text(text='Изменить скидку', ignore_case=True))
async def ask_new_discount(message: Message):
    button_5 = KeyboardButton(text='5')
    button_10 = KeyboardButton(text='10')
    button_15 = KeyboardButton(text='15')
    button_20 = KeyboardButton(text='20')
    button_25 = KeyboardButton(text='25')
    discounts_keyboard = ReplyKeyboardMarkup(keyboard=[[button_5, button_10, button_15, button_20, button_25]], 
                                             resize_keyboard=True, 
                                             one_time_keyboard=True)
    await message.answer('Выберите новое значение:', reply_markup=discounts_keyboard)


# Этот хэндлер будет срабатывать на числа ['5', '10', '15', '20', '25'] и изменять текущий минимальный размер скидки
@dp.message(Text(text=['5', '10', '15', '20', '25']))
async def update_discount(message: Message):
    global current_discount
    new_discount = int(message.text)
    current_discount = new_discount
    await message.answer(f'Нижний порог скидки при поиске изменен на {current_discount}%', reply_markup=ReplyKeyboardRemove())


# Этот хэндлер будет срабатывать на команду "/min" и предлогать показать либо изменить минимальный порог цены
@dp.message(Command(commands=['min']))
async def process_minprice_command(message: Message):
    current_price = KeyboardButton(text='Текущая минимальная цена')
    change_price = KeyboardButton(text='Изменить минимальную цену')
    kb = ReplyKeyboardMarkup(keyboard=[[current_price, change_price]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Выберите действие:', reply_markup=kb)


# Этот хэндлер будет срабатывать на текст 'Текущая минимальная цена' и показывать текущее значение
@dp.message(Text(text='Текущая минимальная цена', ignore_case=True))
async def show_current_discount(message: Message):
    await message.answer(f'Текущая минимальная цена: ${min_price}', reply_markup=ReplyKeyboardRemove())


# Этот хэндлер будет срабатывать на текст 'Изменить минимальную цену' и предлогать выбор из 5 новых значений
@dp.message(Text(text='Изменить минимальную цену', ignore_case=True))
async def ask_new_discount(message: Message):
    button_1 = KeyboardButton(text='500')
    button_2 = KeyboardButton(text='1500')
    button_3 = KeyboardButton(text='2000')
    button_4 = KeyboardButton(text='3000')
    button_5 = KeyboardButton(text='4000')
    min_price_keyboard = ReplyKeyboardMarkup(keyboard=[[button_1, button_2, button_3, button_4, button_5]], 
                                             resize_keyboard=True, 
                                             one_time_keyboard=True)
    await message.answer('Выберите новое значение:', reply_markup=min_price_keyboard)


# Этот хэндлер будет срабатывать на числа ['500', '1500', '2000', '3000', '5000'] и устанавливать их как нижний порог
@dp.message(Text(text=['500', '1500', '2000', '3000', '5000']))
async def update_discount(message: Message):
    global min_price
    new_min_price = int(message.text)
    min_price = new_min_price
    await message.answer(f'Нижний порог цены при поиске изменен на ${min_price}', reply_markup=ReplyKeyboardRemove())


# Этот хэндлер будет срабатывать на команду "/max" и предлогать показать либо изменить максимальный порог цены
@dp.message(Command(commands=['max']))
async def process_minprice_command(message: Message):
    current_price = KeyboardButton(text='Текущая максимальная цена')
    change_price = KeyboardButton(text='Изменить максимальную цену')
    kb = ReplyKeyboardMarkup(keyboard=[[current_price, change_price]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Выберите действие:', reply_markup=kb)


# Этот хэндлер будет срабатывать на текст 'Текущая максимальная цена' и показывать текущее значение
@dp.message(Text(text='Текущая максимальная цена', ignore_case=True))
async def show_current_discount(message: Message):
    await message.answer(f'Текущая максимальная цена: ${max_price}', reply_markup=ReplyKeyboardRemove())


# Этот хэндлер будет срабатывать на текст 'Изменить максимальную цену' и предлогать выбор из 5 новых значений
@dp.message(Text(text='Изменить максимальную цену', ignore_case=True))
async def ask_new_discount(message: Message):
    button_1 = KeyboardButton(text='0')
    button_2 = KeyboardButton(text='5000')
    button_3 = KeyboardButton(text='7500')
    button_4 = KeyboardButton(text='10000')
    button_5 = KeyboardButton(text='15000')
    max_price_keyboard = ReplyKeyboardMarkup(keyboard=[[button_1, button_2, button_3, button_4, button_5]], 
                                             resize_keyboard=True, 
                                             one_time_keyboard=True)

    await message.answer('Выберите новое значение:', reply_markup=max_price_keyboard)


# Этот хэндлер будет срабатывать на числа ['0', '5000', '7500', '10000', '15000'] и устанавливать их как верхний порог
@dp.message(Text(text=['0', '5000', '7500', '10000', '15000']))
async def update_discount(message: Message):
    global max_price
    new_max_price = int(message.text)
    max_price = new_max_price
    await message.answer(f'Верхний порог цены при поиске изменен на ${max_price}', reply_markup=ReplyKeyboardRemove())


# Это хендлер перехватывающий все остальные сообщения
@dp.message()
async def send_echo(message: Message):
    await message.reply(text="Мой функционал ограничен, извините.")


if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    # Запускаем поллинг
    dp.run_polling(bot)