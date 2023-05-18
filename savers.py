from schemas import OzonPrice, OzonCategoryFee
import openpyxl
from openpyxl import Workbook
from datetime import datetime


def save_to_gsheet(ozon_prices: list[OzonPrice]):
    print('MOCK data saved to gsheets')


def save_fbo_dbs_to_excel(ozon_prices: list[OzonPrice]):
    filepath = f'./data/fbo_fbs/fbo_fbs-{datetime.now().date()}.xlsx'
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
    filepath = f'./data/category_fees/category_fees-{datetime.now().date()}.xlsx'
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
