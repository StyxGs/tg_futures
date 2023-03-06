from aiogram import Bot

from services.service import price_future


async def send_notification_message(bot: Bot, chat_id: int, future: str):
    text = await price_future(future)
    await bot.send_message(chat_id=chat_id, text=text)
