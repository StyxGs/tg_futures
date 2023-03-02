# Ответы бота на команды
# Список фьючерсов

LEXICON_RU: dict = {
    '/start': 'Привет, я бот информатор о фьючерсах на бирже <b>binance</b>.\n'
              'Выбери в меню команду /help, для сводки по всем доступным командам',
    '/help': 'Привет, я бот который поможет тебе получать актуальную '
             'информацию о доступных фьючерсах на бирже <b>binance</b>.\n'
             '<b>Доступные команды:</b>\n'
             '/look - покажет данные о последних 3-х сделках\n'
             '/klines - покажет данные по свечам\n'
             '/add - добавить фьючерс в список отслеживаемых\n'
             '/tracked - посмотреть список отслеживаемых фьючерсов\n',
    'del_futures': 'Редактировать фьючерсы',
    'del': '❌',
    'cancel': 'ОТМЕНИТЬ',
    'no_futures': 'Вы не отслеживаете ни один фьючерс.\n'
                  'Напишите команду "<b>/add</b>" ли выберите её в меню, чтоб добавить фьючерсы',
    'about_list_futures': 'Список всех доступных фьючерсов:\n'
                          '(В списке могут быть не все доступные фьючерсы, это связанно с '
                          'ограничениями телеграмма, если не нашли попробуйте отправить в '
                          'чат название фьючерса)',
    'interval': '1m   // 1 минута\n'
                '3m   // 3 минута\n'
                '5m   // 5 минута\n'
                '15m   // 15 минута\n'
                '30m   // 30 минута\n'
                '1h   // 1 час\n'
                '2h   // 2 часа\n'
                '4h   // 4 часа\n'
                '6h   // 6 часов\n'
                '8h   // 8 часов\n'
                '12h   // 12 часов\n'
                '1d   // 1 день\n'
                '3d   // 3 дня\n'
                '1w   // 1 неделя\n'
                '3M   // 1 месяц\n'
}