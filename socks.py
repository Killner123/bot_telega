import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from bs4 import BeautifulSoup
import requests
from difflib import get_close_matches

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
    keyboard.add(types.KeyboardButton('Поиск персонажей'))
    await message.reply(
        "Привет! Я бот поиска персонажей из Hunter x Hunter. Нажми кнопку 'Поиск персонажей', чтобы начать поиск.",
        reply_markup=keyboard
    )
    await state.finish()  # Завершаем любое предыдущее состояние


# Обработка кнопки 'Поиск персонажей'
@dp.message_handler(text='Поиск персонажей')
async def search_character_menu(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('В главное меню'))
    await message.reply(
        "Введите имя персонажа (на русском языке), чтобы получить ссылку на него.",
        reply_markup=keyboard
    )
    await CharacterSearchStates.WaitingForCharacterName.set()  # Устанавливаем состояние ожидания ввода имени персонажа


# Обработка сообщений с текстом
@dp.message_handler(state=CharacterSearchStates.WaitingForCharacterName, content_types=types.ContentType.TEXT)
async def search_character(message: types.Message, state: FSMContext):
    character_name = message.text
    character_name_en = character_name.replace(" ", "_")
    character_category_urls = [
        "https://hunterxhunter.fandom.com/ru/wiki/Категория:Персонажи",
        "https://hunterxhunter.fandom.com/ru/wiki/Категория:Персонажи?from=Сквало"
    ]
    character_list = []

    for character_category_url in character_category_urls:
        response = requests.get(character_category_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            character_links = soup.find_all("div", class_="category-page__members")

            for div in character_links:
                for link in div.find_all("a", href=True):
                    character_list.append(link.text)

    if character_name in character_list:
        character_url = f"https://hunterxhunter.fandom.com/ru/wiki/{character_name_en}"
        reply_message = f"<b>Имя персонажа:</b> {character_name}\n\n"
        reply_message += f"<b>Подробнее:</b> {character_url}"
    else:
        similar_names = get_close_matches(character_name, character_list, n=3, cutoff=0.6)
        if similar_names:
            reply_message = f"Персонаж не найден. Возможно, вы имели в виду одного из следующих персонажей:\n\n"
            reply_message += "\n".join(similar_names)
        else:
            reply_message = "Персонаж не найден. Введите другое имя."

    await message.reply(reply_message, parse_mode='HTML')
    await state.finish()  # Завершаем состояние ожидания ввода имени персонажа


# Обработка кнопки 'В главное меню'
@dp.message_handler(text='В главное меню')
async def main_menu(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Поиск персонажей'))
    await message.reply(
        "Вы вернулись в главное меню. Нажми кнопку 'Поиск персонажей', чтобы начать поиск.",
        reply_markup=keyboard
    )
    await state.finish()  # Завершаем любое предыдущее состояние


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)