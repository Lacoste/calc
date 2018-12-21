import xlrd
import functools

from django import forms
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string

from .base import (BasePriceList, hourly_rates_only_validator,
                   min_price_validator)
from .spreadsheet_utils import generate_column_index_map, safe_cell_str_value
from .coercers import (strip_non_numeric, extract_min_education,
                       extract_hour_unit_of_issue)
from contracts.models import EDUCATION_CHOICES

DEFAULT_SHEET_NAME = 'Service Pricing'

EXAMPLE_SHEET_ROWS = [
    [
        r'SIN(s) PROPOSED',
        r'SERVICE PROPOSED (e.g. Job Title/Task)',
        r'MINIMUM EDUCATION/ CERTIFICATION LEVEL',
        r'MINIMUM YEARS OF EXPERIENCE',
        r'COMMERCIAL LIST PRICE (CPL)   OR MARKET  PRICES',
        r'UNIT OF ISSUE (e.g. Hour, Task, Sq ft)',
        r'MOST FAVORED CUSTOMER (MFC)',
        r'DISCOUNT OFFERED TO MFC (%)',
        r'MFC PRICE',
        r'GSA(%) DISCOUNT (exclusive of the .75% IFF)',
        r'PRICE OFFERED TO GSA (excluding IFF)',
        r'PRICE OFFERED TO GSA (including IFF)',
        r'QUANTITY/VOLUME DISCOUNT',
    ],
    [
        r'712-3',
        r'Project Manager',
        r'High School',
        r'3',
        r'',
        r'',
        r'',
        r'',
        r'',
        r'',
        r'',
        r'95.00',
        r'',
    ],
]

class Region3PriceList(BasePriceList):

    title = 'Region 3'  

    table_template = 'data_capture/price_list/tables/region_3.html'

    upload_example_template = ('data_capture/price_list/upload_examples/'
                               'region_3.html')

    upload_widget_extra_instructions = 'XLS or XLSX format, please.'


    @classmethod
    def get_upload_example_context(cls):
        return {
            'sheet_name': DEFAULT_SHEET_NAME,
            'sheet_rows': EXAMPLE_SHEET_ROWS,
        }