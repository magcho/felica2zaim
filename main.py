# -*- coding: utf-8 -*-
from lib.felica import readFelica
from lib.GasSpread import GasSpread
from lib.Slack import Slack
from lib.Filter import Filter

from lib.zaim.zaimAppendItem import zaimAppendItems

from lib.zaim.oath import oath
from lib.zaim.zaimAppendItem import zaimAppendItems

from pprint import pprint
import json
from time import sleep
import sys


def printList(data):
    print(json.dumps(data, ensure_ascii=False))


def main():
    slackMoney = Slack(
        'https://hooks.slack.com/services/ ** slack webhook endpoint **', ' ** slack channel **')

    try:
        felicaDataList = readFelica(True)
        print('felica read')
    except IndexError as e:
        slackMoney.sendMessage(str(e))

    gas = GasSpread(' ** google spreadsheet token **',
                    '** google spreadsheet auth json file path **')

    felicaDataList = gas.calcPrice(felicaDataList)

    gas.postItems('rawLog', felicaDataList)

    productCount = gas.postItems(
        'products', Filter().buyProduct(felicaDataList))
    publicTransportCount = gas.postItems(
        'publicTransport', Filter().publicTransport(felicaDataList))

    appendZaimApiCount = zaimAppendItems(gas.notExistDbFelicaItemFilter(felicaDataList))
    slackMoney.sendMessage('商品購入:' + str(productCount) +
                           '件 鉄道乗車:' + str(publicTransportCount) +
                           '件 zaim記帳:' + str(appendZaimApiCount))


if __name__ == "__main__":
    try:
        while True:
            try:
                main()
                sleep(1)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
    except KeyboardInterrupt:
        sys.exit(0)
