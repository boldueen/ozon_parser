from datetime import datetime
import pandas as pd

from openpyxl import Workbook

from gsheet_worker import add_data_gsh
from utils import get_prices_as_list, get_fees_as_list
from schemas import OzonPrice, OzonCategoryFee


def save_fbo_fbs_to_gsheet(ozon_prices: list[OzonPrice]):
    data_list = get_prices_as_list(ozon_prices)

    title = ['Объёмный вес', 'fbo_coef', 'fbo_min',
             'fbo_max', 'fbs_coef', 'fbs_min', 'fbs_max']

    df = pd.DataFrame(data_list, columns=title)
    print(df.dtypes)
    add_data_gsh('test_fbo_fbs', df)


def save_fees_to_gsheet(category_fees: list[OzonCategoryFee]):
    data_list = get_fees_as_list(category_fees)

    title = ['Id категории', 'категория',
             'название', 'комиссия', 'процент выкупа']

    df = pd.DataFrame(data_list, columns=title)
    add_data_gsh('test_fee_categories', df)


def save_fbo_dbs_to_excel(ozon_prices: list[OzonPrice]):
    filename = f'fbo_fbs-{int(datetime.now().timestamp())}'
    filepath = f'./data/fbo_fbs/{filename}.xlsx'
    wb = Workbook()
    wb.save(filepath)
    ws = wb.active
    titles = [
        'Объёмный вес',
        'fbo_coeff',
        'fbo_min',
        'fbo_max',
        'fbs_coeff'
        'fbs_min',
        'fbs_max',
    ]
    ws.append(titles)

    for ozon_price in ozon_prices:
        ws.append([
            ozon_price.volume_weight,
            ozon_price.fbo.coefficient,
            ozon_price.fbo.min,
            ozon_price.fbo.max,
            ozon_price.fbs.coefficient,
            ozon_price.fbs.min,
            ozon_price.fbs.max,
        ])
    wb.save(filepath)


def save_category_fees_to_excel(fees: list[OzonCategoryFee]):
    filename = f'category_fees-{int(datetime.now().timestamp())}'
    filepath = f'./data/category_fees/{filename}.xlsx'
    wb = Workbook()
    wb.save(filepath)
    ws = wb.active
    titles = ['id категории', 'категория маркетплейса',
              'название', 'fee', 'процент доставки']
    ws.append(titles)

    for fee in fees:
        ws.append([
            str(fee.base_category.category_id),
            fee.marketplace_category,
            fee.base_category.name,
            fee.fee,
            fee.delivered_percent
        ])
    wb.save(filepath)
