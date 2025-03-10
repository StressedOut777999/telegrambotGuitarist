from sicret import BOT_TOKEN
import asyncio
from data import get_music, get_guitar
import logging
import sys
from os import getenv
from comands import START_BOT_COMMAND, GUITARISTS_BOT_COMMAND
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, URLInputFile
from keyboard import MusicCallback, music_keyboard_markup, keyboard_url
from models import Guitarists_info


# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(Command('guitarists'))
async def command_music_handler(message: Message) -> None:
    music = get_music()
    markup = music_keyboard_markup(music)
    await message.answer(f'топ музиканти', reply_markup=markup)



@dp.message(Command("guitar"))
async def guitar_info(message: Message, command: CommandObject):
    if command.args:
        guitar_name = command.args.lower()
        guitars = get_guitar()
        results = [i for i in guitars if guitar_name in i['name'].lower()]
        if results:
            for i in results:
                await message.answer_photo(caption=f"Знайдено: {html.bold(i['name'])}", photo=i["img"])
        else:
            await message.answer("Гітару не знайдено.")
    else:
        await message.answer("Такої гітари немає")



@dp.callback_query(MusicCallback.filter())
async def callb_film(callback: CallbackQuery, callback_data:MusicCallback) -> None:
    film_id = callback_data.id # 0
    film_info = get_music(music_id=film_id)
    film = Guitarists_info(**film_info)

    text = f"гітарист: {film.name}\n" \
           f"Опис: {film.description}\n" \

    for i in film.instruments: 
        text += f"назва гітари{i.name}"


        await callback.message.answer_photo(caption=text,photo=URLInputFile(i.img), reply_markup=keyboard_url(i.song))



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! ~цей бот показує відомих гітаристів та їх гітари~")


# @dp.message()
# async def echo_handler(message: Message) -> None:
#     """
#     Handler will forward receive a message back to the sender

#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands([START_BOT_COMMAND, GUITARISTS_BOT_COMMAND])
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())






