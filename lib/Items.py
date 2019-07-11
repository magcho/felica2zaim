# -*- coding: utf-8 -*-

from binToInfo import BinToInfo


class Item(object):
    def __init__(self, bin):
        self.binToInfo = BinToInfo()

        self.bin = bin

        self.price = 0

        self.machineType = [
            bin[0],
            self.binToInfo.machineType(bin[0])
        ]
        self.useType = [
            bin[1],
            self.binToInfo.useType(bin[1])
        ]
        self.payType = [
            bin[2],
            self.binToInfo.payType(bin[2])
        ]
        self.gateType = [
            bin[3],
            self.binToInfo.gateType(bin[3])
        ]
        self.balance = int(bin[7])
        self.no = bin[8]
        self.isAppleWatch = (bin[8] <= 2000)  # pasmoの方なら2000件超えてる
        self.isPasmo = (bin[8] > 2000)  # pasmoの方なら2000件超えてる

    def getBinToInfo(self):
        return self.binToInfo


class TransportItem(Item):
    def __init__(self, bin):
        super(TransportItem, self).__init__(bin)
        binToInfo = super(TransportItem, self).getBinToInfo()

        self.date = [
            bin[4],
            {
                'year': (bin[4] >> 9) + 2000,
                'month': (bin[4] >> 5) & 0xF,
                'day': bin[4] & 0x1F,
            }
        ]
        self.enterStation = [
            bin[5],
            binToInfo.readFiveByte(bin[5])
        ]
        self.exitStation = [
            bin[6],
            binToInfo.readSixByte(bin[6])
        ]

        self.isAutoCharge = False
        # オートチャージ処理
        #   オートチャージ時は入場駅がチャージ改札駅で出場駅が西馬込と同じコードになる
        if(self.exitStation[0] == 0x0000):
            if(self.price == 1000):
                self.exitStation[1] = ['オートチャージ', 'odakyu credit']
                self.isAutoCharge = True


class BuyProductItem(Item):
    def __init__(self, bin):
        super(BuyProductItem, self).__init__(bin)
        binToInfo = super(BuyProductItem, self).getBinToInfo()

        self.date = [
            bin[4],
            {
                'year': (bin[4] >> 9) + 2000,
                'month': (bin[4] >> 5) & 0xF,
                'day': bin[4] & 0x1F,
                'hour': (bin[5] >> 9),
                'minute': (bin[5] >> 5) & 0x3F,
                'second': (bin[5] & 0x1F)
            }
        ]
        self.store = [
            bin[6],
            binToInfo.readSixByte(bin[6])
        ]


class OtherItem(Item):
    def __init__(self, bin):
        super(BuyProductItem, self).__init__(bin)
        pass


class Abc(Item):
    pass
