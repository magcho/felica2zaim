# -*- coding: utf-8 -*-
from pprint import pprint

from lib.zaim.oath import oath
from lib.zaim.appendItem import appendItem

from lib.utils import *

def main():

    zaim = oath()




    # res = zaim.get('genre',params={
    #     'mapping': 1
    # })
    # printList(res.json())

    # res = zaim.get('account',params={
    #     'mapping': 1
    # })

    # res = zaim.post('money/payment', {
    #     'mapping': 1,
    #     'category_id': 103,
    #     'genre_id': 10301,
    #     'amount': 1,
    #     'date': '2019-4-3',
    #     'from_account_id': 6,
    #     'comment': 'コメント',
    #     'name': '電車',
    #     'place': '場所'
    # })

    printList(res.json())

main()
