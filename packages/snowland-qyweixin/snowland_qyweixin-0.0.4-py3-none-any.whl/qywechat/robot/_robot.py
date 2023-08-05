# -*- coding: utf-8 -*-

__auth__ = 'A.Star'

import base64
from typing import List, Dict

import requests
from pysmx.crypto import hashlib


class Robot:
    def __init__(self, robot_url):
        self.robot_url = robot_url

    def send_message(self, msgtype, data):
        json_data = {
            "msgtype": msgtype,
            msgtype: data
        }
        res = requests.post(self.robot_url, json=json_data)
        return res.json()

    def send_markdown(self, content="", mentioned_list=None, mentioned_mobile_list=None):
        data = {"content": content}
        if mentioned_list is not None:
            data['mentioned_list'] = mentioned_list
        if mentioned_mobile_list is None:
            data['mentioned_mobile_list'] = mentioned_mobile_list
        return self.send_message("markdown", data)

    def send_text(self, content="", mentioned_list=None, mentioned_mobile_list=None):
        data = {"content": content}
        if mentioned_list is not None:
            data['mentioned_list'] = mentioned_list
        if mentioned_mobile_list is None:
            data['mentioned_mobile_list'] = mentioned_mobile_list
        return self.send_message("text", data)

    def send_image(self, image, mentioned_list=None, mentioned_mobile_list=None):
        data = {}
        if isinstance(image, bytes):
            image_json = {}
            b64_image = base64.b64encode(image)
            image_json["data"] = b64_image
            md5 = hashlib.md5()
            md5.update(image)
            image_json["md5"] = md5.hexdigit()
        if mentioned_list is not None:
            data['mentioned_list'] = mentioned_list
        if mentioned_mobile_list is None:
            data['mentioned_mobile_list'] = mentioned_mobile_list
        return self.send_message("image", data)

    def send_news(self, articles: List[Dict], mentioned_list=None, mentioned_mobile_list=None):

        for article in articles:
            assert "title" in article
            assert "description" in article
            assert "url" in article
            assert "picurl" in article
        data = {"articles": articles}
        if mentioned_list is not None:
            data['mentioned_list'] = mentioned_list
        if mentioned_mobile_list is None:
            data['mentioned_mobile_list'] = mentioned_mobile_list
        return self.send_message("news", data)
