import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

dp = Dispatcher()
load_dotenv()


class Booking(StatesGroup):
    service = State()
    date = State()
    time = State()
    name = State()
    phone = State()


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    builder = InlineKeyboardBuilder()
    builder.button(text='Осмотр', callback_data='service_Осмотр')
    builder.button(text='Чистка', callback_data='service_Чистка')
    builder.button(text='Лечение', callback_data='service_Лечение')
    builder.adjust(1)

    await message.answer(
        "Здравствуйте! Пожалуйста, выберите услугу:",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data.startswith('service_'))
async def service_callback(callback: types.CallbackQuery, state: FSMContext):
    service = callback.data.split('_')[1]
    await state.update_data(service=service)
    await callback.answer(f"Вы выбрали: {service}")

    # В дальнейшем будут показываться кнопки с датами
    await callback.message.edit_text(
        f"Вы выбрали: {service}\nТеперь выберите дату:",
        # reply_markup=date_kb()
    )


@dp.message(Command("hello"))
async def cmd_hello(message: Message):
    await message.answer(
        f"Привет, <b>{message.from_user.full_name}</b>",
        parse_mode=ParseMode.HTML
    )


@dp.message(Command('help'))
async def cmd_help(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text='Официальный сайт', url='https://ya.ru')
    builder.button(text='Почта: delta_help@yandex.ru', callback_data='email_info')
    builder.adjust(1)

    await message.answer(
        "Ссылки для связи:",
        reply_markup=builder.as_markup()
    )


async def main():
    token = getenv("BOT_TOKEN")
    if not token:
        raise ValueError("No token provided")

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    print("Starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        print("Bot stopped")


if __name__ == '__main__':
    asyncio.run(main())