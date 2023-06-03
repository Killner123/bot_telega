from aiogram import types
from aiogram.dispatcher import FSMContext
from bs4 import BeautifulSoup
import requests
from difflib import get_close_matches
from aiogram.dispatcher.filters.state import State, StatesGroup
from main_menu import main_menu

class CharacterSearchStates(StatesGroup):
    WaitingForCharacterName = State()


async def search_character_menu(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('В главное меню 🚀'))
    await message.reply(
        "Введите имя персонажа (на русском языке), чтобы получить ссылку на него ☕.",
        reply_markup=keyboard
    )
    await CharacterSearchStates.WaitingForCharacterName.set()  # Устанавливаем состояние ожидания ввода имени персонажа


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


    if character_name == 'В главное меню 🚀':
        async def main_menu(message: types.Message, state: FSMContext):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton('Поиск персонажей 🔍'))
            keyboard.add(types.KeyboardButton('Случайный факт 🎲'))
            await message.reply(
                "Вы вернулись в главное меню.",
                reply_markup=keyboard
            )
            await state.finish()  # Завершаем любое предыдущее состояние

        await main_menu(message, state)
    elif character_name:
        if character_name in character_list:
            character_url = f"https://hunterxhunter.fandom.com/ru/wiki/{character_name_en}"
            reply_message = f"<b>Имя персонажа:</b> {character_name}\n\n"
            reply_message += f"<b>Подробнее:</b> {character_url}"
            await message.reply(reply_message, parse_mode='HTML')
        else:
            similar_names = get_close_matches(character_name, character_list, n=10, cutoff=0.4)
            if similar_names:
                reply_message = f"Персонаж не найден. Возможно, вы имели в виду одного из следующих персонажей:\n\n"
                reply_message += "\n".join(similar_names)
            else:
                reply_message = "Персонаж не найден. Введите другое имя🗿."
            await message.reply(reply_message)
    else:
        await message.reply("Введите имя персонажа.")
        return

    if character_name == 'В главное меню 🚀':
        async def main_menu(message: types.Message, state: FSMContext):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton('Поиск персонажей 🔍'))
            keyboard.add(types.KeyboardButton('Случайный факт 🎲'))
            await message.reply(
                "Вы вернулись в главное меню.",
                reply_markup=keyboard
            )
            await state.finish()  # Завершаем любое предыдущее состояние