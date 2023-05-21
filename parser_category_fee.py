import asyncio
from aiohttp import ClientSession
from schemas import ReqCatFee

from utils import get_category_body, get_headers, extract_category_fee_from_response, get_category_ids
from savers import save_category_fees_to_excel

import json
from savers import save_fees_to_gsheet


categories = []


async def parse_category_fee(category: ReqCatFee, session):
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
    print('start parsing categories_fee... .. .')
    categories_objs = await get_category_ids()
    tasks = []
    async with ClientSession() as session:
        for categories_obj in categories_objs:
            task = asyncio.create_task(
                parse_category_fee(categories_obj, session))
            tasks.append(task)
        await asyncio.gather(*tasks)

    sorted_categories = sorted(categories)
    print(f"PARSED {len(sorted_categories)} values")

    save_category_fees_to_excel(sorted_categories)
    print(f"SAVED TO EXCEL")

    save_fees_to_gsheet(sorted_categories)
    print(f"SAVED TO G_SHEETS")


if __name__ == '__main__':
    asyncio.run(main())
