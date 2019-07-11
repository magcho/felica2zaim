# -*- coding: utf-8 -*-
import requests
import json


class Slack:
    def __init__(self, endpointUrl, channelName):
        self.ENDPOINT = endpointUrl
        self.CHANNEL_NAME = channelName

    def sendMessage(self, text):
        responce = requests.post(self.ENDPOINT, data=json.dumps({
            'channel': self.CHANNEL_NAME,
            'text': text,
            'username': 'MoneyBot',
            'icon_emoji': ':robot:',
            'link_names': True,
        }))

        return responce.text
