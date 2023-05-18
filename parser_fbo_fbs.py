from aiohttp import ClientSession
from schemas import OzonPrice

from utils import get_volume_weight_body, get_headers, extract_prices_from_response
from savers import save_fbo_dbs_to_excel

import asyncio
import numpy as np

import json
from pprint import pprint

ozon_prices: list[OzonPrice] = []


async def parse_price(volume_weight: float, session):
    async with session.post(
        'https://seller.ozon.ru/api/site/calculator-ozon-ru/calculator/coefficient_ovh',
            json=await get_volume_weight_body(volume_weight),
            headers=await get_headers()
    ) as raw_response:

        response = json.loads(await raw_response.text())
        print(raw_response.status, volume_weight)

        ozon_price = await extract_prices_from_response(volume_weight, response)
        ozon_prices.append(ozon_price)


async def main():
    volume_weights = [round(x, 2) for x in np.arange(0.1, 35.1, 0.1)]
    tasks = []
    async with ClientSession() as session:
        for volume_weight in volume_weights:
            task = asyncio.create_task(parse_price(volume_weight, session))
            tasks.append(task)
        await asyncio.gather(*tasks)

    pprint(sorted(ozon_prices))
    save_fbo_dbs_to_excel(sorted(ozon_prices))

if __name__ == '__main__':
    asyncio.run(main())
