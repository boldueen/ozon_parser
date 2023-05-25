import json
import requests

from schemas import OzonPrice, TypePrice, OzonCategoryFee, ReqCatFee


async def get_volume_weight_body(volume_weight: float) -> dict:
    return {"volumeWeight": volume_weight}


async def get_headers() -> dict:
    return {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        'Accept': 'application/json, text/plain, */*'
    }


async def extract_prices_from_response(volume_weight: float, response: dict) -> OzonPrice:
    fbo_obj = response.get('fbo')
    fbs_obj = response.get('fbs')
    return OzonPrice(
        volume_weight=volume_weight,
        fbs=TypePrice(coefficient=fbo_obj.get('coefficient', 0),
                      min=fbo_obj.get('min', 0), max=fbo_obj.get('max', 0)),
        fbo=TypePrice(coefficient=fbs_obj.get('coefficient', 0),
                      min=fbs_obj.get('min', 0), max=fbs_obj.get('max', 0))
    )


async def get_req_cat_fee(category_obj: dict) -> ReqCatFee:
    return ReqCatFee(
        name=category_obj.get('name'),
        category_id=category_obj.get('id'),
        level=category_obj.get('level')
    )


async def get_category_ids() -> list[ReqCatFee]:
    categories_for_response = []
    raw_response = requests.post(
        'https://seller.ozon.ru/api/site/calculator-ozon-ru/calculator/tree', headers=await get_headers()
    )

    categories = json.loads(raw_response.text).get('items')

    for cat_lvl_1 in categories:
        categories_for_response.append(await get_req_cat_fee(cat_lvl_1))

        for cat_lvl_2 in cat_lvl_1.get('children'):
            categories_for_response.append(await get_req_cat_fee(cat_lvl_2))
            if len(cat_lvl_2.get('children', [])) == 0:
                break

            for cat_lvl_3 in cat_lvl_2.get('children'):
                categories_for_response.append(await get_req_cat_fee(cat_lvl_3))
                if len(cat_lvl_3.get('children', [])) == 0:
                    break

            for cat_lvl_4 in cat_lvl_3.get('children'):
                categories_for_response.append(await get_req_cat_fee(cat_lvl_4))
                if len(cat_lvl_4.get('children', [])) == 0:
                    break

    print(categories_for_response, len(categories_for_response))
    return categories_for_response


async def get_category_body(category: ReqCatFee):
    return {
        'categoryId': category.category_id,
        'level': category.level
    }


async def extract_category_fee_from_response(category: ReqCatFee, response: dict) -> OzonCategoryFee:
    ozon_cat_fee = OzonCategoryFee(
        base_category=category,
        marketplace_category=response.get('marketplaceCategory'),
        fee=response.get('fee'),
        delivered_percent=response.get('deliveredPercent')
    )
    return ozon_cat_fee


def get_fees_as_list(data: list[OzonCategoryFee]) -> list:
    response = []
    for obj in data:
        response.append([
            obj.base_category.category_id,
            obj.marketplace_category,
            obj.base_category.name,
            obj.fee,
            obj.delivered_percent
        ])
    return response


def get_prices_as_list(data: list[OzonPrice]) -> list:
    response = []
    for obj in data:
        print(obj)
        response.append([
            obj.volume_weight,
            obj.fbo.coefficient,
            obj.fbo.min,
            obj.fbo.max,
            obj.fbs.coefficient,
            obj.fbs.min,
            obj.fbs.max,
        ])
    return response
