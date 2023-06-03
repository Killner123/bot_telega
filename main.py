import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from search_character import search_character_menu, search_character
from aiogram.dispatcher import FSMContext
import random
from main_menu import main_menu

# Инициализация бота и диспетчера
bot = Bot(token="5302190487:AAGgfGCwZ4niNbw0FZyinVIrE2IDdAgo5-E")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)


class CharacterSearchStates(StatesGroup):
    WaitingForCharacterName = State()  # Состояние ожидания ввода имени персонажа


# Обработка команды /start
@dp.message_handler(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Поиск персонажей 🔍'))
    keyboard.add(types.KeyboardButton('Случайный факт 🎲'))  # Добавляем кнопку "Случайный факт"
    await message.reply(
        "Привет! Я бот Энигма! 🔰.",
        reply_markup=keyboard
    )
    await state.finish()  # Завершаем любое предыдущее состояние



# Обработка кнопки 'Поиск персонажей'
@dp.message_handler(text='Поиск персонажей 🔍')
async def search_character_handler(message: types.Message, state: FSMContext):
    await search_character_menu(message, state)


# Обработка сообщений с текстом
@dp.message_handler(state=CharacterSearchStates.WaitingForCharacterName, content_types=types.ContentType.TEXT)
async def search_character_handler(message: types.Message, state: FSMContext):
    await search_character(message, state)


async def send_random_fact(message: types.Message):
    with open('facts.txt', 'r', encoding='utf-8') as file:
        facts = file.read().splitlines()
    random_fact = random.choice(facts)
    await message.answer(random_fact)

# Добавляем обработчик команды для запроса случайного факта
@dp.message_handler(text='Случайный факт 🎲')
async def get_random_fact(message: types.Message):
    await send_random_fact(message)



# Запуск бота
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
