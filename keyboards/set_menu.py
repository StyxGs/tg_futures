# Формирование меню

from aiogram import Bot
from aiogram.types import BotCommand


async def set_menu(bot: Bot):
    """Добавляет и формирует меню"""
    main_menu_commands = [
        BotCommand(command='/help', description='Краткая сводка по командам'),
        BotCommand(command='/add', description='Добавить фьючерс в список отслеживаемых'),
        BotCommand(command='/tracked', description='Отслеживаемые фьючерсы'),
        BotCommand(command='/look', description='Данные о последних 3 сделках'),
        BotCommand(command='/klines', description='Данные по свечам'),
        BotCommand(command='/24hr', description='Статистика за последние 24 часа'),
        BotCommand(command='/best_price', description='Лучшая цена покупки/продажи'),
        BotCommand(command='/price_notification', description='Задать оповещение о цене'),
    ]
    await bot.set_my_commands(main_menu_commands)
