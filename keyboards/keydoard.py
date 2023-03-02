# Создание кнопок для времени

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

time_keyboards: InlineKeyboardBuilder = InlineKeyboardBuilder()

time_keyboards.row(InlineKeyboardButton(text='5 минут', callback_data='5'),
                   InlineKeyboardButton(text='10 минут', callback_data='10'),
                   InlineKeyboardButton(text='20 минут', callback_data='20'),
                   InlineKeyboardButton(text='30 минут', callback_data='30'),
                   InlineKeyboardButton(text='40 минут', callback_data='40'),
                   InlineKeyboardButton(text='50 минут', callback_data='50'),
                   InlineKeyboardButton(text='1 час', callback_data='60'),
                   InlineKeyboardButton(text='2 часа', callback_data='120'),
                   InlineKeyboardButton(text='3 часа', callback_data='180'),
                   InlineKeyboardButton(text='5 часов', callback_data='300'),
                   InlineKeyboardButton(text='отменить', callback_data='cancel'),
                   width=2)

time_list = ['5', '10', '15', '20', '30', '40', '50', '60', '120', '180', '300']
