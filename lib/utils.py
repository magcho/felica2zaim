# -*- coding: utf-8 -*-

import json


def printList(data):
    print(json.dumps(data, ensure_ascii=False))


def isExists(var):
    try:
        var
    except NameError:
        return False
    return True
