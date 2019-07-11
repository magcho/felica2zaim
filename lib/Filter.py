# -*- coding: utf-8 -*-
from Items import BuyProductItem, TransportItem, OtherItem


class Filter:
    def buyProduct(self, felicaDataList):
        returnBuff = []
        for item in felicaDataList:
            if(isinstance(item, BuyProductItem)):
                returnBuff.append(item)
        return returnBuff

    def publicTransport(self, felicaDataList):
        returnBuff = []
        for item in felicaDataList:
            if(isinstance(item, TransportItem)):
                returnBuff.append(item)
        return returnBuff

    def other(self, felicaDataList):
        returnBuff = []
        for item in felicaDataList:
            if(isinstance(item, OtherItem)):
                returnBuff.append(item)
        return returnBuff
