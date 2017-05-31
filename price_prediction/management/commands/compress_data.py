#building off of calc/contracts/management/commands
import asyncio
import math
from datetime import datetime
from django.core.management import BaseCommand
from optparse import make_option
from django.core.management import call_command
import numpy as np
from price_prediction.models import LaborCategory, CompressedData
from inflation_calc import inflation
import datetime as dt

def is_nan(obj):
    if type(obj) == type(float()):
        return math.isnan(obj)
    else:
        return False


async def main(category, years): 
    data = LaborCategory.objects.filter(labor_category=category).all()
    base_year = years[0]
    for year in years:
        #convert prices to base year
        prices = []
        for elem in data:
            if elem.date.year==year:
                if float(elem.price) > 501.00 or is_nan(float(elem.price)):
                    continue
                else:
                    #price = inflation.inflate(round(float(elem.price),2), dt.date(year=year,month=1,day=1), dt.date(year=base_year, month=1, day=1), 'United States')
                    compressed_data = CompressedData(price=round(float(elem.price), 2),year=year)
                    compressed_data.save()

class Command(BaseCommand):
    #do year over year analysis
    def handle(self, *args, **options):
        labor_data = LaborCategory.objects.all()
        categories = list(set([elem.labor_category for elem in labor_data]))
        years = list(set([int(elem.date.year) for elem in labor_data]))
        years.sort()
        loop = asyncio.get_event_loop()
        for category in categories:
            loop.run_until_complete(main(category, years))
        loop.close()
        
        