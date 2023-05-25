import json
import asyncio

from aiohttp import ClientSession
import numpy as np

from schemas import OzonPrice
from savers import save_fbo_fbs_to_gsheet, save_fbo_dbs_to_excel
from utils import get_volume_weight_body, get_headers, extract_prices_from_response

ozon_prices: list[OzonPrice] = []


async def parse_price(volume_weight: float, session):

    for _ in range(10):
        async with session.post(
            'https://seller.ozon.ru/api/site/calculator-ozon-ru/calculator/coefficient_ovh',
                json=await get_volume_weight_body(volume_weight),
                headers=await get_headers()
        ) as raw_response:
            if raw_response.status == 200:
                response = json.loads(await raw_response.text())
                print(raw_response.status, volume_weight)

                ozon_price = await extract_prices_from_response(volume_weight, response)
                ozon_prices.append(ozon_price)
                return

    print(f'[ERROR] unable to parse wolume_weight={volume_weight}')


async def main():
    volume_weights = [round(x, 2) for x in np.arange(0.1, 35.1, 0.1)]
    tasks = []
    async with ClientSession() as session:
        for volume_weight in volume_weights:
            task = asyncio.create_task(parse_price(volume_weight, session))
            tasks.append(task)
        await asyncio.gather(*tasks)

    sorted_ozon_prices = sorted(ozon_prices)
    print(f"PARSED {len(sorted_ozon_prices)} values")
    save_fbo_dbs_to_excel(sorted_ozon_prices)
    print(f"SAVED TO EXCEL")
    save_fbo_fbs_to_gsheet(sorted_ozon_prices)
    print(f"SAVED TO G_SHEETS")


if __name__ == '__main__':
    asyncio.run(main())
