import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.set_menu import set_menu
from middlewares.apscheduler import ApschedulerMiddleware

# Инициализируем логгер
logger = logging.getLogger(__name__)


async def main():
    """Функция для запуска бота"""

    # Конфигурация логгера
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s'
    )

    # Выводим в консоль лог о старте бота
    logger.info('Starting bot')

    # Загружаем конфигруцию бота
    config: Config = load_config()

    # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
    storage: MemoryStorage = MemoryStorage()

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tgbot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)

    apscheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    apscheduler.start()

    # Загружаем роутары
    dp.update.middleware.register(ApschedulerMiddleware(apscheduler))
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Главное меню бота
    await set_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
