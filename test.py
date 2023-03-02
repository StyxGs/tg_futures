import asyncio

import aiohttp


async def ty():
    url = 'https://fapi.binance.com/fapi/v1/ticker/price'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    tasc1 = asyncio.create_task(ty())

    await tasc1

tr = asyncio.run(main())
