# -*- coding: utf-8 -*-

from oath import oath

from ..Items import TransportItem, BuyProductItem
from ..utils import *


def zaimAppendItems(items):
    zaim = oath()
    successItemCount = 0
    for item in items:
        if(not item.isPasmo):
            # mobileSuicaはzaim側で自動取得されるのでここでは記帳しない
            continue
        if(isinstance(item, TransportItem)):
            if(item.isAutoCharge):
                continue

            date = str(item.date[1]['year']) + '-' + str(item.date[1]
                                                         ['month']) + '-' + str(item.date[1]['day'])
            comment = str(item.enterStation[1][2]) + \
                '-' + str(item.exitStation[1][2])
            place = comment
            # pasmo: 11686459
            # suica: 11662998
            payload = {
                'mapping': 1,
                'category_id': 103,  # 交通
                'genre_id': 10301,  # 電車
                'amount': item.price * -1,
                'date': date,
                'from_account_id': 11686459,
                'comment': comment,
                'name': '電車',
                'place': '交通機関'
            }
            zaim.post('money/payment', payload)
            successItemCount = successItemCount + 1

        elif(isinstance(item, BuyProductItem)):
            date = str(item.date[1]['year']) + '-' + str(item.date[1]
                                                         ['month']) + '-' + str(item.date[1]['day'])
            payload = {
                'mapping': 1,
                'category_id': 101,  # 食費
                'genre_id': 10104,  # お昼飯
                'amount': item.price * -1,
                'date': date,
                'from_account_id': 11686459,
                'comment': 'IC購入',
                'name': 'IC購入',
                'place': str(item.store[1][0]) + str(item.store[1][1])
            }
            zaim.post('money/payment', payload)
            successItemCount = successItemCount + 1

    return successItemCount
