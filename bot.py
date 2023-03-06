import asyncio
import logging
import aioredis

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator

from config.config import Config, load_config, jobstores
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
    # Инициализируем Redis
    redis = await aioredis.from_url(url=f'redis://bot_redis:6379', db=0)

    # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
    storage: RedisStorage = RedisStorage(redis)

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tgbot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)

    # Инициализируем apscheduler

    apscheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone='Europe/Moscow', jobstores=jobstores))
    apscheduler.ctx.add_instance(bot, declared_class=Bot)
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
