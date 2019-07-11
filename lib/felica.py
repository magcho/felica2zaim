# -*- coding: utf-8 -*-
import nfc
import binascii
from pprint import pprint
import struct
import requests
import json

from binToInfo import isTransport, isBuyProduct
from Items import TransportItem, BuyProductItem, OtherItem


def readFelica(f_debug=False):
    bin = _fetchFelica()
    responce = _purseBin(bin)

    felicaItems = []
    for item in reversed(responce):
        try:
            if(isTransport(item)):
                lineBuff = TransportItem(item)
            elif(isBuyProduct(item)):
                lineBuff = BuyProductItem(item)
            else:
                print(item)
                raise IndexError('undefined item type')
        except IndexError as e:
            print(e)
        felicaItems.append(lineBuff)

    return felicaItems


def _fetchFelica():
    FELICA_DATA_SIZE = 20
    SERVICE_CODE = 0x090f  # 決済履歴保存ブロックのサービスコード
    buff = []

    device = nfc.clf.ContactlessFrontend('usb')
    targetFelica = nfc.clf.RemoteTarget("212F")  # 212 = 212bit/s, F = Felica
    targetFelica.sensf_req = bytearray.fromhex("0000030000")  # 交通系ICの呼び出し

    try:
        responce = device.sense(targetFelica, iterations=100, interval=0.2)
        if(responce != None):
            tag = nfc.tag.activate(device, responce)
            for i in range(FELICA_DATA_SIZE):
                sc = nfc.tag.tt3.ServiceCode(
                    SERVICE_CODE >> 6, SERVICE_CODE & 0x1f)
                bc = nfc.tag.tt3.BlockCode(i, service=0)
                data = tag.read_without_encryption([sc], [bc])
                buff.append(data)
            return buff
        else:
            raise ValueError('can\'t read responce')
    except ValueError as e:
        print(e)


def _purseBin(data):
    buff = []

    for line in data:
        lineBuff = []

        bigEndi = struct.unpack('>4B4HBHB', bytes(line))
        littleEndi = struct.unpack('<4B4HBHB', bytes(line))

        lineBuff.append(bigEndi[0])  # 機器種別
        lineBuff.append(bigEndi[1])  # 利用種別
        lineBuff.append(bigEndi[2])  # 決済種別
        lineBuff.append(bigEndi[3])  # 入出場種別
        lineBuff.append(bigEndi[4])  # 年月日
        lineBuff.append(bigEndi[5])  # 入出場駅コード(鉄道)、停留所コード(バス)、物販情報(物販)
        lineBuff.append(bigEndi[6])  # 決済情報1
        lineBuff.append(littleEndi[7])  # 残高
        lineBuff.append(bigEndi[9])  # 決済No.(連番)
        lineBuff.append(bigEndi[10])  # 地域コード

        buff.append(lineBuff)
    return buff
