from datetime import datetime

import aiohttp

URL = 'https://fapi.binance.com/fapi/v1/'


async def string_available_transaction_data(ft: str) -> str:
    """Узнает данные о последних 3 сделках по переданному фьючерсу"""
    async with aiohttp.ClientSession() as session:
        async with session.get(URL + 'trades', params={'symbol': ft, 'limit': 3}) as response:
            deals = await response.json()
            if isinstance(deals, list):
                v = ''
                for i in deals:
                    v += (f'<b>Цена по которой состоялась сделка:</b> {i["price"]}\n<b>Id сделки</b>: {i["id"]}\n'
                          f'<b>Количество в сделке:</b> {i["qty"]}\n<b>Сумма сделки</b>: {i["quoteQty"]}\n'
                          f'<b>Время сделки:</b> {datetime.fromtimestamp(int(i["time"] / 1000))}\n'
                          f'<b>{"Сделка по покупке" if i["isBuyerMaker"] else "Сделка по продаже"}</b>\n\n')
                return v
            else:
                return 'Возможно вы некорректно ввели название фьючерса, попробуйте снова. /look'


async def string_available_klines_data(ft: str) -> str:
    """Узнает данные о свечах по переданному фьючерсу и лимиту времни"""
    data = await _check_value(ft)
    name, interval = data
    params = {'symbol': name.upper(), 'limit': 1, 'interval': interval.lower()}
    async with aiohttp.ClientSession() as session:
        async with session.get(URL + 'klines', params=params) as response:
            kline = await response.json()
            if isinstance(kline, list):
                v = ''
                for i in kline:
                    v += f'<b>Время открытия:</b> {datetime.fromtimestamp(int(i[0] / 1000))}\n' \
                         f'<b>Цена открытия:</b> {i[1]}\n' \
                         f'<b>Максимальная цена:</b> {i[2]}\n' \
                         f'<b>Минимальная цена:</b> {i[3]}\n' \
                         f'<b>Цена закрытия:</b> {i[4]}\n' \
                         f'<b>Объем:</b> {i[5]}\n' \
                         f'<b>Время закрытия:</b> {datetime.fromtimestamp(int(i[6] / 1000))}\n' \
                         f'<b>Объем квотируемой валюты:</b> {i[7]}\n' \
                         f'<b>Кол-во сделок:</b> {i[8]}\n\n'

                return v
            else:
                return 'Возможно вы некорректно ввели название фьючерса или интервала, попробуйте снова. /klines'


async def statistics_for_24hr(ft: str) -> str:
    """Узнаёт статистику за последние 24 часа по фьючерсу"""
    async with aiohttp.ClientSession() as session:
        async with session.get(URL + 'ticker/24hr', params={'symbol': ft}) as response:
            response = await response.json()
            if len(response) > 2:
                return f'<b>Изменение цены за сутки:</b> {response["priceChange"]}\n' \
                       f'<b>Изменение цены за сутки в %:</b> {response["priceChangePercent"]}%\n' \
                       f'<b>Средневзвешенная цена:</b> {response["weightedAvgPrice"]}\n' \
                       f'<b>Последняя цена:</b> {response["lastPrice"]}\n' \
                       f'<b>Последний объем:</b> {response["lastQty"]}\n' \
                       f'<b>Цена открытия:</b> {response["openPrice"]}\n' \
                       f'<b>Самая высокая цена:</b> {response["highPrice"]}\n' \
                       f'<b>Самая низкая цена:</b> {response["lowPrice"]}\n' \
                       f'<b>Объем торгов базовой валюты:</b> {response["volume"]}\n' \
                       f'<b>Объем торгов квотируемой валюты:</b> {response["quoteVolume"]}\n' \
                       f'<b>Время открытия:</b> {datetime.fromtimestamp(int(response["openTime"] / 1000))}\n' \
                       f'<b>Время закрытия:</b> {datetime.fromtimestamp(int(response["closeTime"] / 1000))}\n' \
                       f'<b>Кол-во сделок:</b> {response["count"]}'
            else:
                return 'Возможно вы некорректно ввели название фьючерса или интервала, попробуйте снова. /24hr'


async def best_price(ft: str) -> str:
    """Узнаёт лучшую цену покупки/продажи"""
    async with aiohttp.ClientSession() as session:
        async with session.get(URL + 'ticker/bookTicker', params={'symbol': ft}) as response:
            response = await response.json()
            if len(response) > 2:
                return f'<b>Лучшая цена покупки:</b> {response["bidPrice"]}\n' \
                       f'<b>Кол-во к покупке:</b> {response["bidQty"]}\n' \
                       f'<b>Лучшая цена продажи:</b> {response["askPrice"]}\n' \
                       f'<b>Кол-во к продаже:</b> {response["askQty"]}'
            else:
                return 'Возможно вы некорректно ввели название фьючерса или интервала, попробуйте снова. /24hr'


async def list_futures_for_button() -> list:
    """Отдаёт список всех фьючерсов на бирже"""
    async with aiohttp.ClientSession() as session:
        async with session.get(URL + 'ticker/price') as response:
            response = await response.json()
            list_futures = []
            for future in response:
                list_futures.append(future['symbol'])
            return list_futures


async def price_future(ft: str) -> str:
    """Отдаёт строку с данными по последнее цене на бирже"""
    async with aiohttp.ClientSession() as session:
        async with session.get(URL + 'ticker/price', params={'symbol': ft}) as response:
            response = await response.json()
            if 'symbol' in response:
                return f'Последняя цена на бирже:\n' \
                       f'<b>{response["symbol"]} - {response["price"]}</b>'
            else:
                return 'Возможно вы некорректно ввели название фьючерса или интервала, попробуйте снова. /24hr'


async def _check_value(value: str) -> list:
    """Проверяет, что переданные данные корректны"""
    data = value.split()
    if len(data) == 2:
        return data
    else:
        return ['0', '0']
