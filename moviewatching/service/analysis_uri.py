#!/usr/bin/env python
# -*- coding: utf-8 -*-
__filename__ = "analysis_uri.py"
__author__ = "worker name."
__version__ = "v0.* - for your version."
__data__ = "2021/12/13"
__time__ = "17:16:00"
__email__ = "****@***.com"
__status__ = "Development"
__message__ = " - vip解析连接管理 - "
__update__ = "What you think can be updated and optimized can be written here"

import random

from flask import current_app

from .untils.pymongo_util import PyMongoUtil


class AnalysisUri:

    def __init__(self):
        self.analysis_collection = PyMongoUtil(
            uri=current_app.config.get("MONGO_URI"),
            db=current_app.config.get("MONGODB_DB"),
            collection=current_app.config.get("MONGODB_TABLE_ANALYSIS_URI")
        )

    def get_one(self, **kwargs):
        """
            例：kwargs={uri:"ddddd"}
        :param kwargs:
        :return:
        """
        return self.analysis_collection.find(kwargs)

    def get_random_one(self):
        """
            随机获取一条
        :return:
        """
        _count = self.analysis_collection.__len__()
        search_id = random.randint(0, 100) % _count
        print(self.analysis_collection.find_one({"id": search_id}, {"_id": 0}))
        return self.analysis_collection.find_one({"id": search_id}, {"_id": 0})

    def get_all(self):
        return self.analysis_collection.find_all()

    def delete_one(self):
        return self.analysis_collection.delete()


if __name__ == "__main__":
    trans = AnalysisUri()
    print(trans.get_random_one())
