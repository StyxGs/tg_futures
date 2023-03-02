# Добавление в список фьючерсов для отслеживания
# редактирования списка

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from lexicon.lexicon import LEXICON_RU
from services.service import list_futures_for_button


async def create_tracked_list(list_futures: list) -> InlineKeyboardBuilder:
    """Создание инлайн-кнопки из отслеживаемых фьючерсов"""
    my_futures_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    futures_buttons = []
    for future in list_futures:
        futures_buttons.append(InlineKeyboardButton(text=future, callback_data=f'{future}*'))

    my_futures_kb.row(*futures_buttons, width=3)
    my_futures_kb.row(InlineKeyboardButton(text=LEXICON_RU['del_futures'], callback_data='del_futures'))
    return my_futures_kb


async def delete_future(list_futures: list) -> InlineKeyboardBuilder:
    """Создание инлайн-кнопки для удаления отслеживаемых фьючерсов"""
    futures_del_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    futures_buttons = []
    for future in list_futures:
        futures_buttons.append(InlineKeyboardButton(text=f'{LEXICON_RU["del"]} {future}',
                                                    callback_data=f'{future}del'))

    futures_del_kb.row(*futures_buttons, width=3)
    futures_del_kb.row(InlineKeyboardButton(text=LEXICON_RU['cancel'], callback_data='cancel'))
    return futures_del_kb


async def list_of_available_futures() -> InlineKeyboardBuilder:
    """Создание инлайн-кнопки для просмотра достпуных фьючерсов"""
    button_list: InlineKeyboardBuilder = InlineKeyboardBuilder()
    button_list.add(InlineKeyboardButton(text='Выбрать фьючерс из списка',
                                         callback_data='list_of_available_futures'))
    return button_list


async def formation_of_futures_buttons() -> InlineKeyboardBuilder:
    """Формирует инлайн кнопки из всех доступных фьючерсов"""
    futures_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    prlist = []
    for future in await list_futures_for_button():
        prlist.append(InlineKeyboardButton(text=future,
                                           callback_data=f'*{future}'))
    futures_kb.row(*prlist, width=3)
    return futures_kb
