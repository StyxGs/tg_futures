from aiogram import Bot

from services.service import price_future


async def send_notification_message(bot: Bot, chat_id: int, future: str):
    await bot.send_message(chat_id=chat_id, text=price_future(future))
