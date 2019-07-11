# -*- coding: utf-8 -*-

from stationCode import stationCodedic
from buyProductCode import buyProductCodeDicC7, buyProductCodeDicC8


class BinToInfo:

    useTypeInfo = ''
    machineTypeCode = ''

    def machineType(self, bin):
        self.machineTypeCode = bin
        dic = {
            0x3: "乗り越し精算機",
            0x5: "バス/路面電車等",
            0x7: "自動販売機",
            0x8: "自動券売機",
            0x9: "SMART ICOCAクイックチャージ機",
            0x12: "自動券売機",
            0x14: "駅窓口",
            0x15: "定期券券売機",
            0x16: "自動改札機",
            0x17: "簡易改札機",
            0x18: "駅窓口",
            0x19: "窓口処理機(有人改札)",
            0x1A: "窓口処理機(有人改札)",
            0x1B: "パソリ等",
            0x1C: "のりこし精算機",
            0x1D: "他社線のりかえ自動改札機",
            0x1F: "入金機、簡易入金機",
            0x20: "窓口端末(名鉄)",
            0x21: "精算機",
            0x22: "窓口処理機/簡易改札機/バス等 (カード種類ごとに異なる用途がある模様)",
            0x23: "新幹線改札機",
            0x24: "車内補充券発行機",
            0x46: "VIEW ALTTE、特典など",
            0x48: "ポイント交換機(nimoca)",
            0xC7: "物販/タクシー等",
            0xC8: "物販/タクシー等"
        }
        if bin in dic:
            return dic[bin]
        else:
            raise IndexError('undefined machineTypeCode => ' + dic)

    def useType(self, bin):
        if(bin > 128):
            # 電子マネーと現金の併用決済
            self.F_combindRealMoney = True
            bin = bin - 128
        else:
            self.F_combindRealMoney = False

        trainCodes = [1, 2, 20, 22, 29]
        productSalesCodes = [70, 73, 74, 75, 198, 199, 200, 203]
        busCodes = [13, 15, 31, 35]
        if bin in trainCodes:
            self.useTypeInfo = 'train'
        elif bin in productSalesCodes:
            self.useTypeInfo = 'product'
        elif bin in busCodes:
            self.useTypeInfo = 'bus'

        dic = {
            0x01: "自動改札機出場/有人改札出場",
            0x02: "SFチャージ",
            0x03: "乗車券類購入",
            0x04: "精算(乗り越し等)",
            0x05: "精算(乗り越し等)",
            0x06: "窓口出場",
            0x07: "新規",
            0x08: "チャージ控除(返金)",
            0x09: 'チャージ機',
            0x0C: "バス/路面等(均一運賃?)",
            0x0D: "バス/路面等(均一運賃)",
            0x0F: "バス/路面等",
            0x10: "再発行?",
            0x11: "再発行?",
            0x12: '発券機',
            0x13: "自動改札機出場?(新幹線)",
            0x14: "オートチャージ",
            0x17: "オートチャージ(PiTaPa)",
            0x19: "バスの精算?",
            0x1A: "バスの精算?",
            0x1B: "バスの精算 (障害者割引などの精算)",
            0x1D: "リムジンバス等",
            0x1F: "チャージ(バス/窓口)、チャージ機(OKICA)",
            0x23: "乗車券類購入 (都バスIC一日乗車券など)",
            0x33: "取り消し(残高返金)",
            0x46: "物販",
            0x48: "ポイントチャージ",
            0x49: "SFチャージ(物販扱い)",
            0x4A: "物販の取消",
        }

        if bin in dic:
            return {
                'info': dic[bin],
                'combindRealMoney': self.F_combindRealMoney
            }
        else:
            raise IndexError('undefined useTypeCode => ' + str(bin))

    def payType(self, bin):
        dic = {
            0x00: "通常決済",
            0x02: "VIEWカード",
            0x0B: "PiTaPa(物販等)",
            0x0C: "一般のクレジットカード?",
            0x0D: "パスネット/PASMO",
            0x13: "nimoca (nimocaポイント交換機でのクイックチャージ)",
            0x1E: "nimoca (チャージ時のSF還元)",
            0x3F: "モバイルSuicaアプリ(クレジットカード)",
        }

        if bin in dic:
            return dic[bin]
        else:
            raise IndexError('undefined payTypeCode => ' + str(bin))

    def gateType(self, bin):

        dic = {
            0x00: "通常出場および精算以外(新規、チャージ、乗車券類購入、物販等)",
            0x01: "入場(オートチャージ)",
            0x02: "入場+出場(SF)",
            0x03: "定期入場→乗り越し精算出場(SF)",
            0x04: "定期券面前乗車入場(SF)→定期出場",
            0x05: "乗継割引(鉄道)",
            0x08: '控除 (窓口控除)',
            0x0E: "窓口出場",
            0x0F: "バス/路面等の精算",
            0x17: "乗継割引(バス→鉄道?)",
            0x1D: "乗継割引(バス)",
            0x21: "乗継精算(筑豊電鉄 指定駅乗継、熊本市交通局 辛島町電停 A系統↔B系統など)",
            0x22: "券面外乗降?",
        }

        if bin in dic:
            return dic[bin]
        else:
            raise IndexError('undefined gateTypeCode => ' + str(bin))

    def date(self, bin):
        return {
            'year': (bin >> 9) + 2000,
            'month': (bin >> 5) & 0xF,
            'day': bin & 0x1F
        }

    def readFiveByte(self, bin):
        """入出場駅コード(鉄道)、停留所コード(バス)、物販情報(物販)

        Parameters
        ----------
        bin : String


        Returns
        -------
        dict
            [駅名, 路線名]

        """
        if self.useTypeInfo == 'train':
            if bin in stationCodedic:
                return stationCodedic[bin]
            else:
                raise IndexError('undefined stationCode => ' + str(bin))
            return bin

        if self.useTypeInfo == 'product':
            if self.machineTypeCode == 0xC7:
                if bin in buyProductCodeDicC7:
                    return buyProductCodeDicC7[bin]
                else:
                    # raise IndexError('undefined storeCode => ' + str(bin))
                    return ['storeCode 未登録', str(bin)]
            elif self.machineTypeCode == 0xC8:
                if bin in buyProductCodeDicC8:
                    return buyProductCodeDicC8[bin]
                else:
                    # raise IndexError('undefined storeCode => ' + str(bin))
                    return ['storeCode 未登録', str(bin)]
            else:
                raise IndexError('undefined useType for product =>' + str(bin))

        if self.useTypeInfo == 'bus':
            return 'バス利用 バス停コード' + str(bin)
        else:
            raise IndexError('undefined useType')

    def readSixByte(self, bin):
        return self.readFiveByte(bin)


def isTransport(bin):
    transportCodes = [1, 13, 15, 31, 35, 20, 22, 27, 29]
    for i in transportCodes:
        if(bin[0] == i):
            return True
    else:
        return False


def isBuyProduct(bin):
    productSalesCodes = [70, 73, 74, 75, 198, 199, 200, 203]
    for i in productSalesCodes:
        if(bin[0] == i):
            return True
    return False
