from aiohttp import ClientSession
from schemas import OzonPrice, TypePrice, ReqCatFee

from utils import get_category_body, get_headers, extract_category_fee_from_response, get_category_ids
from savers import save_category_fees_to_excel

import asyncio
import numpy as np

import json
from pprint import pprint

categories = []


async def parse_category_fee(category: ReqCatFee, session) -> OzonPrice:
    async with session.post(
        'https://seller.ozon.ru/api/site/calculator-ozon-ru/calculator/values_by_category',
            json=await get_category_body(category),
            headers=await get_headers()
    ) as raw_response:
        print(raw_response.status, category.category_id, category.name)

        if raw_response.status == 200:
            response = json.loads(await raw_response.text())
            print(raw_response.status, category.category_id, category.name)

            category = await extract_category_fee_from_response(category, response)
            categories.append(category)


async def main():
    categories_objs = await get_category_ids()
    tasks = []
    async with ClientSession() as session:
        for categories_obj in categories_objs:
            task = asyncio.create_task(
                parse_category_fee(categories_obj, session))
            tasks.append(task)
        await asyncio.gather(*tasks)

    pprint(len(categories))
    save_category_fees_to_excel(categories)

if __name__ == '__main__':
    asyncio.run(main())
