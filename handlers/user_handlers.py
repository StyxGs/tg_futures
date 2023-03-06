from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ContentType, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import db
from handlers.shedulers import send_notification_message
from keyboards.keydoard import time_keyboards, time_list
from keyboards.tracked_list import (create_tracked_list, delete_future,
                                    formation_of_futures_buttons,
                                    list_of_available_futures)
from lexicon.lexicon import LEXICON_RU
from services.service import (best_price, list_futures_for_button,
                              price_future, statistics_for_24hr,
                              string_available_klines_data,
                              string_available_transaction_data)
from services.statesform import WriteFuture

router = Router()
BotDB = db.BotDB()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    """Ответ на команду start и добавление пользователя в базу данных, если его нет"""
    await message.answer(LEXICON_RU['/start'])
    await BotDB.check_user_in_db(message.from_user.id)


@router.message(Command(commands=['help']))
async def help_command(message: Message) -> None:
    """Ответ на команду help"""
    await message.answer(LEXICON_RU['/help'])


@router.message(Command(commands=['look']))
async def look_command(message: Message, state: FSMContext) -> None:
    """Отправляет сообщение с просьбой ввести название фьючерса и вводит в состояние"""
    await state.set_state(WriteFuture.transaction_data)
    await message.answer(text='Введите название интересующего вас фьючерса или введите команду <b>"отменить"</b>')


@router.message(F.text.casefold().lower() == "отменить", WriteFuture)
async def cancel_state(message: Message, state: FSMContext) -> None:
    """Выводит из состояния"""
    await message.answer(text='Команда отменена')
    await state.clear()


@router.message(WriteFuture.transaction_data, F.content_type == ContentType.TEXT)
async def write_future(message: Message, state: FSMContext) -> None:
    """Отправляет данные о последних 3-х сделок"""
    text = await string_available_transaction_data(message.text.upper())
    await message.answer(text=text)
    await state.clear()


@router.message(WriteFuture.transaction_data)
async def wrong_to_write_future(message: Message) -> None:
    """Реагирует, если пользователь отправил тип сообщение не текстового
    формата находясь в состоянии"""
    await message.answer(text='Отправьте текстовое сообщение с название фьючерса')


@router.message(Command(commands=['klines']))
async def look_command(message: Message, state: FSMContext) -> None:
    """Отправляет сообщение с просьбой ввести название фьючерса, лимита времени и вводит в состояние"""
    await state.set_state(WriteFuture.klines_data)
    await message.answer(
        text=f'Введите название интересующего вас фьючерса и интересующий вас интервал '
             f'или введите команду <b>"отменить"</b>.\n\n'
             f'Пример: LTCBTC 5m\n\n'
             f'Доступные интервалы:\n\n'
             f'{LEXICON_RU["interval"]}'
    )


@router.message(WriteFuture.klines_data, F.content_type == ContentType.TEXT)
async def write_future(message: Message, state: FSMContext) -> None:
    """Отображает данные о свече и выводит из состояния"""
    text = await string_available_klines_data(message.text)
    await message.answer(text=text)
    await state.clear()


@router.message(WriteFuture.klines_data)
async def wrong_to_write_future(message: Message) -> None:
    """Реагирует, если пользователь отправил тип сообщение не текстового
    формата находясь в состоянии"""
    await message.answer(text='Отправьте текстовое сообщение с названием фьючерса и интервалом')


@router.message(Command(commands=['24hr']))
async def look_command(message: Message, state: FSMContext) -> None:
    """Включает состояния ввода фьючерса"""
    await state.set_state(WriteFuture.statistics_24hr)
    await message.answer(text='Введите название интересующего вас фьючерса или введите команду <b>"отменить"</b>')


@router.message(WriteFuture.statistics_24hr, F.content_type == ContentType.TEXT)
async def write_future(message: Message, state: FSMContext) -> None:
    """Отображает данные за 24 часа и выводит из состояния"""
    text = await statistics_for_24hr(message.text)
    await message.answer(text=text)
    await state.clear()


@router.message(WriteFuture.statistics_24hr)
async def wrong_to_write_future(message: Message) -> None:
    """Реагирует, если пользователь отправил тип сообщение не текстового
    формата находясь в состоянии"""
    await message.answer(text='Отправьте текстовое сообщение с названием фьючерса')


@router.message(Command(commands=['best_price']))
async def look_command(message: Message, state: FSMContext) -> None:
    """Включает состояния ввода фьючерса"""
    await state.set_state(WriteFuture.best_price)
    await message.answer(text='Введите название интересующего вас фьючерса или введите команду <b>"отменить"</b>')


@router.message(WriteFuture.best_price, F.content_type == ContentType.TEXT)
async def write_future(message: Message, state: FSMContext) -> None:
    """Отправляет сообщение с лучшей ценой продажи/покупки"""
    text = await best_price(message.text)
    await message.answer(text=text)
    await state.clear()


@router.message(WriteFuture.best_price)
async def wrong_to_write_future(message: Message) -> None:
    """Реагирует, если пользователь отправил тип сообщение не текстового
    формата находясь в состоянии"""
    await message.answer(text='Отправьте текстовое сообщение с названием фьючерса')


@router.message(Command(commands=['add']))
async def add_to_my_list(message: Message, state: FSMContext) -> None:
    """Даёт возможность добавить фьючерс в список"""
    await state.set_state(WriteFuture.choice_future)
    keyboard = await list_of_available_futures()
    await message.answer(text='Отправьте текстовое сообщение с названием фьючерса',
                         reply_markup=keyboard.as_markup())


@router.callback_query(Text(text='list_of_available_futures'))
async def show_list_futures(callback: CallbackQuery) -> None:
    """Показывает список всех доступных фьючерсов"""
    keyboard = await formation_of_futures_buttons()
    await callback.message.edit_text(text=LEXICON_RU['about_list_futures'],
                                     reply_markup=keyboard.as_markup(), cache_time=3600)


@router.callback_query(lambda x: x.data[0] == '*')
async def add_future_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """Добавить в фьючерс в список отлеживаемых через кнопку"""
    future = callback.data.upper()
    await BotDB.add_future_in_list(callback.from_user.id, future[1:])
    await callback.answer(text='Фьючерс добавлен в список')
    await state.clear()


@router.message(WriteFuture.choice_future, F.content_type == ContentType.TEXT)
async def add_future_message(message: Message, state: FSMContext) -> None:
    """Добавить в фьючерс в список отлеживаемых через сообщение"""
    future = message.text
    futures = await list_futures_for_button()
    if future.upper() in futures:
        await BotDB.add_future_in_list(message.from_user.id, future.upper())
        await message.answer(text='Фьючерс добавлен в список')
    else:
        await message.answer(text='Возможно вы некорректно ввели название фьючерса попробуйте снова.')
    await state.clear()


@router.message(WriteFuture.choice_future)
async def wrong_to_write_future(message: Message) -> None:
    """Реагирует, если пользователь отправил тип сообщение не текстового
    формата находясь в состоянии"""
    await message.answer(text='Отправьте текстовое сообщение с названием фьючерса')


@router.message(Command(commands=['tracked']))
async def show_my_list_futures(message: Message) -> None:
    """Отправить список отслеживаемых фьючерсов из инлайн-кнопок"""
    my_futures = await BotDB.show_my_list_futures(message.from_user.id)
    if my_futures:
        keyboard = await create_tracked_list(my_futures)
        await message.answer(text='Ваши фьючерсы:', reply_markup=keyboard.as_markup())
    else:
        await message.answer(text='Вы не отслеживаете ни один фьючерс')


@router.message(Command(commands=['price_notification']))
async def show_my_list_futures_for_notification(message: Message, state: FSMContext) -> None:
    """Состояния добавления оповещение по фьючерсу"""
    my_futures = await BotDB.show_my_list_futures(message.from_user.id)
    if my_futures:
        keyboard = await create_tracked_list(my_futures)
        await state.set_state(WriteFuture.notification)
        await message.answer(text='Выберите фьючерс:', reply_markup=keyboard.as_markup())
    else:
        await message.answer(text='Вы не отслеживаете ни один фьючерс. Добавить? /add')


@router.callback_query(WriteFuture.notification, lambda x: x.data[-1] == '*')
async def choice_interval_notification(callback: CallbackQuery, state: FSMContext):
    """Отдаёт список выбора интервала времени оповещений"""
    await state.update_data(future=callback.data[:-1])
    await callback.message.edit_text(text='Выберите интервал оповещения:', reply_markup=time_keyboards.as_markup())


@router.callback_query(WriteFuture.notification, lambda x: x.data in time_list)
async def add_interval_notification(callback: CallbackQuery, state: FSMContext, apscheduler: AsyncIOScheduler,
                                    bot: Bot):
    """Задаёт интервал оповещения о цене"""
    context_data = await state.get_data()
    time = int(callback.data)
    future = context_data.get('future')
    if future not in [ft.id for ft in apscheduler.get_jobs()]:
        apscheduler.add_job(send_notification_message, trigger='interval', minutes=time,
                            kwargs={'chat_id': callback.from_user.id, 'future': future},
                            id=f'{future}{callback.from_user.id}')
        await callback.message.edit_text(text='Интервал задан. Оповещение добавлено!')
    else:
        apscheduler.reschedule_job(job_id=future, trigger='interval', minutes=time)
        await callback.message.edit_text(text='Интервал изменён!')
    await state.clear()


@router.callback_query(lambda x: x.data[-1] == '*')
async def press_future_in_my_futures_list(callback: CallbackQuery) -> None:
    """Отправляет цену фьючерса на бирже в данный момент"""
    await callback.answer()
    text = await price_future(callback.data[0:-1])
    await callback.message.answer(text=text)


@router.callback_query(Text(text='del_futures'))
async def show_for_deletion_future_in_my_list_futures(callback: CallbackQuery) -> None:
    """Отправляет список фьючерсов для удаления"""
    my_futures = await BotDB.show_my_list_futures(callback.from_user.id)
    if my_futures:
        keyboard = await delete_future(my_futures)
        await callback.message.edit_text(text='Выберите фьючерс для удаления:',
                                         reply_markup=keyboard.as_markup())


@router.callback_query(lambda x: x.data[-3:] == 'del')
async def cancel_deletion_future(callback: CallbackQuery, apscheduler: AsyncIOScheduler, ) -> None:
    """Удаляет фьючерс из списка отслеживаемых"""
    future = callback.data[:-3]
    await BotDB.delete_future_in_my_list(callback.from_user.id, future)
    my_futures = await BotDB.show_my_list_futures(callback.from_user.id)
    if my_futures:
        keyboard = await delete_future(my_futures)
        await callback.message.edit_text(text='Выберите фьючерс для удаления:',
                                         reply_markup=keyboard.as_markup())
        # Проверяет задано ли оповещение о выбранном фьючерсе, если да то удаляет и его
        if f'{future}{callback.from_user.id}' in [ft.id for ft in apscheduler.get_jobs()]:
            apscheduler.remove_job(job_id=f'{future}{callback.from_user.id}')
    else:
        await callback.message.edit_text(text='Вы не отслеживаете ни один фьючерс')


@router.callback_query(Text(text='cancel'))
async def press_cancel(callback: CallbackQuery) -> None:
    """Отменяет редактирования списка"""
    my_futures = await BotDB.show_my_list_futures(callback.from_user.id)
    keyboard = await create_tracked_list(my_futures)
    await callback.message.edit_text(text='Ваши фьючерсы:', reply_markup=keyboard.as_markup())
