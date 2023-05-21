from schemas import OzonPrice, OzonCategoryFee
import pygsheets
from pandas import DataFrame

from config import SERVICE_FILE, TABLE_NAME


def add_data_gsh(name_sheet: str, data: DataFrame, start=(1, 1)):
    sh = open_connection()
    wks = get_work_space(sh, name_sheet)
    print(wks.url)
    wks.clear(fields='*')
    wks.set_dataframe(data, start)
    wks.adjust_column_width(1, 26)


def aplay_standart_format(wks, ranges=['A1:Z1'], color={
    "red": 0.27,
    "green": 0.505,
    "blue": 0.55
}, font_color={
    "red": 1,
    "green": 1,
    "blue": 1
}):
    wks.apply_format(ranges=ranges, format_info={
        "backgroundColorStyle": {
            "rgbColor": color},
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE",
        "textFormat": {
            "fontSize": 10,
            "foregroundColorStyle": {
                "rgbColor": font_color
            }},
        "padding": {
            "top": 18,
            "right": 15,
            "bottom": 18,
            "left": 15
        }
    })


def add_data_gsh_with_wks(wks, data, start=(1, 1)):
    wks.set_dataframe(data, start)


def open_connection():
    gc = pygsheets.authorize(service_file=SERVICE_FILE)
    sh = gc.open(TABLE_NAME)

    return sh


def create_list_if_not_exist(sh, sheet):
    for sheet_v in sh._sheet_list:
        if sheet_v.title == sheet:
            return
    sh.add_worksheet(sheet)


def get_work_space(sh, sheet):
    create_list_if_not_exist(sh, sheet)
    return sh.worksheet_by_title(sheet)


def update_with_of_table(wks):
    wks.adjust_column_width(1, 26)


def get_custom_work_space(sh, sheet):
    wks = get_work_space(sh, sheet)

    wks.apply_format(['A2:Z'], format_info={
        "horizontalAlignment": "CENTER",
        "padding": {
            "top": 5,
            "right": 5,
            "bottom": 5,
            "left": 5
        }
    })
    wks.apply_format(
        ranges=[
            'G2:G',
            'J2:J',
            'L2:L',
            'N2:N',
            'P2:P',
            'R2:R',
            'T2:T',
            'V2:V'],
        format_info={
            "backgroundColorStyle": {
                "rgbColor": {
                    "red": 1,
                    "green": 0.9,
                    "blue": 0.8
                }},
            "numberFormat": {"type": "PERCENT"},
            "horizontalAlignment": "CENTER"
        })
    wks.apply_format(['A2:A', 'B2:B', ], ["DATE", "TIME"])
    wks.apply_format(ranges=['A1:Z1'], format_info={
        "backgroundColorStyle": {
            "rgbColor": {
                "red": 0.27,
                "green": 0.505,
                "blue": 0.55
            }},
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE",
        "textFormat": {
            "fontSize": 10,
            "foregroundColorStyle": {
                "rgbColor": {
                    "red": 1,
                    "green": 1,
                    "blue": 1
                }
            }},
        "padding": {
            "top": 18,
            "right": 15,
            "bottom": 18,
            "left": 15
        }
    })
    return wks
