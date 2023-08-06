# -*- coding:utf-8 -*-
import re


pattern = re.compile(r'<[^>]+>', re.S)


def remove_html(text):
    result = pattern.sub('', text)
    return result
