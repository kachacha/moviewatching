#!/usr/bin/env python
# -*- coding: utf-8 -*-
__filename__ = "test.py"
__author__ = "worker name."
__version__ = "v0.* - for your version."
__data__ = "2021/12/10"
__time__ = "20:28:00"
__email__ = "****@***.com"
__company__ = "唯一视觉"
__status__ = "Development"
__message__ = "Your writing completion status and other information can be written here"
__update__ = "What you think can be updated and optimized can be written here"

import os
import sys


def line_file_test():
    print(sys._getframe().f_lineno)  # 获取当前行号(行数)

    print(__file__)  # 获得当前Python文件绝对路径
    print(os.path.basename(__file__))  # 获得当前Python文件文件名


print(line_file_test())
import random

search_id = random.randint(0, 100) % 5
print(search_id)
