from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class MusicCallback(CallbackData, prefix='music', sep=';'):
    id: int
    name: str


def music_keyboard_markup(music_list:list[dict], offset:int|None=None,
                         skip:int|None=None):
    builder = InlineKeyboardBuilder()
    builder.adjust(1, repeat=True)
    for index, music_data in enumerate(music_list):
        callback_data = MusicCallback(id=index, **music_data)
        builder.button(text=f"{callback_data.name}", callback_data=callback_data.pack())
    builder.adjust(1, repeat=True)
    return builder.as_markup()


def keyboard_url(url):
    builder = InlineKeyboardBuilder()
    builder.button(text="Перейти за посиланням", url=str(url))
    return builder.as_markup()