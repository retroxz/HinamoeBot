#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@Author         : retroxz
@Date           : 2021/9/24 22:20
@Description    : None
@GitHub         : https://github.com/retroxz
"""
__author__ = "retroxz"

import qrcode
import base64
from io import BytesIO

"""
    二维码相关
"""


def generate_bili_auth_qr(login_url):
    auth_qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=3
    )
    auth_qr.add_data(login_url)
    auth_qr.make()
    qr_img = auth_qr.make_image()

    # 转base64
    buffer = BytesIO()
    qr_img.save(buffer, format='png')
    base64_str = base64.b64encode(buffer.getvalue()).decode()
    return base64_str
