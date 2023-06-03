from aiogram import types
from aiogram.dispatcher import FSMContext

async def main_menu(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Поиск персонажей 🔍'))
    await message.reply(
        "Вы вернулись в главное меню.",
        reply_markup=keyboard
    )
    await state.finish()  # Завершаем любое предыдущее состояние
