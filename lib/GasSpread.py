# -*- coding: utf-8 -*-
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import gspread

from Items import *
from utils import *


class GasSpread:
    def __init__(self, sheetKeyCode, credentialJsonFilePath):
        self.sheetKeyCode = sheetKeyCode
        self.credentialJsonFilePath = credentialJsonFilePath

        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        json_file = self.credentialJsonFilePath  # OAuth用クライアントIDの作成でダウンロードしたjsonファイル
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            json_file, scopes=scopes)
        http_auth = credentials.authorize(Http())

        client = gspread.authorize(credentials)
        self.workSheets = client.open_by_key(self.sheetKeyCode)

        sheetId = self._getSheetId('calc')
        wsheet = self.workSheets.get_worksheet(sheetId)
        self.maxNo = {}
        self.maxNo['pasmo'] = wsheet.acell('B1').value
        self.maxNo['suica'] = wsheet.acell('B2').value

        sheetId = self._getSheetId('calc')
        wsheet = self.workSheets.get_worksheet(sheetId)
        self.lastDBbalance = {}
        self.lastDBbalance['pasmo'] = int(wsheet.acell('B4').value)
        self.lastDBbalance['suica'] = int(wsheet.acell('B5').value)

    def postItems(self, postTarget, items):
        if(postTarget == 'products'):
            sendListBuff = []
            for item in items:
                if(self._DBexistItem(item)):
                    continue

                sendBuff = []

                sendBuff.append(item.date[1]['month'])  # 月
                sendBuff.append(item.date[1]['day'])  # 日
                sendBuff.append(item.date[1]['hour'])  # 時
                sendBuff.append(item.date[1]['minute'])  # 分
                sendBuff.append(item.date[1]['second'])  # 秒

                sendBuff.append(item.store[1][0])  # 店名1
                sendBuff.append(item.store[1][1])  # 店名2

                if(item.isPasmo):  # pasmoならNo.2000超えている
                    sendBuff.append('pasmo')  # 利用端末
                    sendBuff.append(item.price)
                    sendBuff.append(item.balance)
                    sendBuff.append('')
                    sendBuff.append(item.no)
                else:
                    sendBuff.append('mobile Suica')  # 利用端末
                    sendBuff.append(item.price)
                    sendBuff.append('')
                    sendBuff.append(item.balance)
                    sendBuff.append('')
                    sendBuff.append(item.no)

                sendListBuff.append(sendBuff)

        elif(postTarget == 'publicTransport'):
            sendListBuff = []
            for item in items:
                if(self._DBexistItem(item)):
                    continue
                sendBuff = []

                sendBuff.append(item.date[1]['year'])
                sendBuff.append(item.date[1]['month'])
                sendBuff.append(item.date[1]['day'])

                sendBuff.append(item.enterStation[1][2])  # 乗車駅
                sendBuff.append(item.enterStation[1][1])  # 乗車路線

                sendBuff.append('→')

                if(item.price > 0):
                    # チャージ処理
                    sendBuff.append('チャージ')
                    sendBuff.append('')
                else:
                    sendBuff.append(item.exitStation[1][2])  # 降車駅
                    sendBuff.append(item.exitStation[1][1])  # 降車路線

                if(item.isPasmo):
                    sendBuff.append('PASMO')
                else:
                    sendBuff.append('Mobile Suica')

                sendBuff.append(item.price)  # 乗車賃

                if(item.isPasmo):
                    sendBuff.append(item.balance)
                    sendBuff.append('')
                    sendBuff.append(item.no)
                else:
                    sendBuff.append('')
                    sendBuff.append(item.balance)
                    sendBuff.append('')
                    sendBuff.append(item.no)

                sendListBuff.append(sendBuff)

        elif(postTarget == 'rawLog'):
            sendPasmoListBuff = []
            sendSuicaListBuff = []

            for item in items:
                if(self._DBexistItem(item)):
                    continue
                sendBuff = []

                sendBuff.append(item.no)
                sendBuff.append(item.date[1]['year'])
                sendBuff.append(item.date[1]['month'])
                sendBuff.append(item.date[1]['day'])

                if(isinstance(item, BuyProductItem)):
                    sendBuff.append(item.date[1]['hour'])
                    sendBuff.append(item.date[1]['minute'])
                    sendBuff.append(item.date[1]['second'])
                else:
                    for i in range(3):
                        sendBuff.append('')

                sendBuff.append(item.balance)
                sendBuff.append(item.price)
                for bin in item.bin:
                    sendBuff.append(bin)

                if(item.isPasmo):
                    sendPasmoListBuff.append(sendBuff)
                else:
                    sendSuicaListBuff.append(sendBuff)

            self._appendItems('rawLog/pasmo', sendPasmoListBuff)
            self._appendItems('rawLog/suica', sendSuicaListBuff)

            return len(sendSuicaListBuff) + len(sendPasmoListBuff)

        return self._appendItems(postTarget, sendListBuff)

    def calcPrice(self, items):
        # 最初のアイテムはDBの残高からの差分
        returnBuff = []

        if(items[0].isPasmo):
            items[0].price = items[0].balance - self.lastDBbalance['pasmo']
        else:
            items[0].price = items[0].balance - self.lastDBbalance['suica']
        returnBuff.append(items[0])

        lastBalance = items[0].balance
        for item in items[1:]:
            item.price = item.balance - lastBalance
            lastBalance = item.balance
            returnBuff.append(item)

        return returnBuff

    def notExistDbFelicaItemFilter(self, items):
        returnBuff = []
        for item in items:
            if(not self._DBexistItem(item)):
                returnBuff.append(item)
        return returnBuff

    def _getWorkSheetList(self):
        return self.workSheets.worksheets()

    def _getSheetId(self, sheetName):
        sheetList = self._getWorkSheetList()
        for sheetObj in sheetList:
            if sheetObj.title == sheetName:
                return sheetList.index(sheetObj)
        return None

    def _appendItems(self, sheetName, items):
        sheetId = self._getSheetId(sheetName)
        wsheet = self.workSheets.get_worksheet(sheetId)
        for item in items:
            wsheet.append_row(item)
        return len(items)

    def _DBexistItem(self, item):
        if(item.no > 2000):
            return int(item.no) <= int(self.maxNo['pasmo'])
        else:
            return int(item.no) <= int(self.maxNo['suica'])
