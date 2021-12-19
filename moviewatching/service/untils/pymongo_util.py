#!/usr/bin/env python
# -*- coding: utf-8 -*-
__filename__ = "pymongo_util.py"
__author__ = "worker name."
__version__ = "v0.* - for your version."
__data__ = "2021/12/13"
__time__ = "14:35:00"
__email__ = "****@***.com"
__status__ = "Development"
__message__ = "pymongo库的封装"
__update__ = "What you think can be updated and optimized can be written here"

import pprint

from pymongo import MongoClient


# MONGODB_USERNAME = os.environ.get("MONGODB_DB", "zfeno")
# MONGODB_PASSWORD = os.environ.get("MONGODB_DB", "jiehuai.qing")
# MONGODB_URI = os.environ.get("MONGO_URI", "mongodb://{0}:{1}@49.234.34.225:27017/"
#                              .format(MONGODB_USERNAME, MONGODB_PASSWORD))


class PyMongoUtil:
    def __init__(self, uri="mongodb://127.0.0.1:27017/", db='VideoPlus', collection='analysis_uri'):
        """初始化MongoDB数据库和表的信息并连接数据库

        :param uri: 连接名
        :param db: 数据库名
        :param collection: 表名
        """
        client = MongoClient(uri)
        self.db = client[db]  # 数据库
        self.collection = self.db[collection]  # 表
        # print(uri, db, collection)
        try:
            if db not in client.list_database_names():
                print("数据库不存在！")
            if collection not in self.db.list_collection_names():
                print("表不存在！")
        except Exception as e:
            print("链接不到数据库：" + uri, "error:" + str(e))

    def __str__(self):
        """数据库基本信息"""
        db = self.db.name
        collection = self.collection.name
        num = self.collection.estimated_document_count()
        return "数据库{} 表{} 共{}条数据".format(db, collection, num)

    def __len__(self):
        """表的数据条数"""
        return self.collection.estimated_document_count()

    def count(self):
        """表的数据条数"""
        return len(self)

    def count_kwargs(self, **kwargs):
        """
        返回查询的条数
        :param kwargs:
        :return:
        """
        n = self.collection.count_documents(kwargs)
        # n = db.test_collection.count_documents({'i': {'$gt': 1000}})
        print('%s documents in collection' % n)
        return n

    def insert(self, *args, **kwargs):
        """插入多条数据

        :param args: 多条数据，可以是dict、dict的list或dict的tuple
        :param kwargs: 单条数据，如name=XerCis, gender=male
        :return: 添加的数据在库中的_id
        """
        documents = []
        for i in args:
            if isinstance(i, dict):
                documents.append(i)
            else:
                documents += [x for x in i]
        documents.append(kwargs)
        return self.collection.insert_many(documents)

    def delete(self, *args, **kwargs):
        """删除一批数据

        :param args: 字典类型，如{"gender": "male"}
        :param kwargs: 直接指定，如gender="male"
        :return: 已删除条数
        """
        # TODO(XerCis) 增加正则表达式
        list(map(kwargs.update, args))
        result = self.collection.delete_many(kwargs)
        return result.deleted_count

    def update(self, *args, **kwargs):
        """更新一批数据

        :param args: dict类型的固定查询条件如{"author":"XerCis"}，循环查询条件一般为_id列表如[{'_id': ObjectId('1')}, {'_id': ObjectId('2')}]
        :param kwargs: 要修改的值，如country="China", age=22
        :return: 修改成功的条数
        """
        value = {"$set": kwargs}
        query = {}
        n = 0
        list(map(query.update, list(filter(lambda x: isinstance(x, dict), args))))  # 固定查询条件
        for i in args:
            if not isinstance(i, dict):
                for _id in i:
                    query.update(_id)
                    result = self.collection.update_one(query, value)
                    n += result.modified_count
        result = self.collection.update_many(query, value)
        return n + result.modified_count

    def update_or_creat(self, *args, **kwargs):
        """更新一批数据 （没有或不存在则创建数据）

        :param args: dict类型的固定查询条件如{"author":"XerCis"}，循环查询条件一般为_id列表如[{'_id': ObjectId('1')}, {'_id': ObjectId('2')}]
        :param kwargs: 要修改的值，如country="China", age=22
        :return: 修改成功的条数
        """
        value = {"$set": kwargs}
        query = {}
        n = 0
        list(map(query.update, list(filter(lambda x: isinstance(x, dict), args))))  # 固定查询条件
        for i in args:
            if not isinstance(i, dict):
                for _id in i:
                    query.update(_id)
                    result = self.collection.update_one(query, value, True)
                    n += result.modified_count
        result = self.collection.update_many(query, value, True)
        return n + result.modified_count

    def replace_id(self, _id, **new_doc):
        """
        通过ID进行更新
        :param _id:
        :param new_doc:
        :return:
        """
        old_document = self.collection.find_one({'_id': _id})
        if old_document:
            result = self.collection.replace_one({'_id': _id}, new_doc)
            print('replaced %s document' % result.modified_count)
            # new_document = self.collection.find_one({'_id': _id})
            # print('document is now %s' % pprint.pformat(new_document))
            return {'status': 'ok', 'info': str(_id) + ':: replace ok !!!'}
        else:
            return {'status': 'fail', 'info': str(_id) + ':: not exist !!!'}

    def replace(self, *condition, **new_doc):
        """
        分步骤通过一定条件进行替换部分内容
        :param condition:
        :param new_doc:
        :return:
        """
        old_document = self.collection.find_one(condition)
        _id = old_document['_id']
        result = self.collection.replace_one({'_id': _id}, new_doc)
        print('replaced %s document' % result.modified_count)
        new_document = self.collection.find_one({'_id': _id})
        print('document is now %s' % pprint.pformat(new_document))

    def find(self, *args, **kwargs):
        """保留原接口"""
        return self.collection.find(*args, **kwargs)

    def find_all(self, show_id=False):
        """所有查询结果

        :param show_id: 是否显示_id，默认不显示
        :return:所有查询结果
        """
        if not show_id:
            return [i for i in self.collection.find({}, {"_id": 0})]
        else:
            return [i for i in self.collection.find({})]

        # def find_all(self, collection, sort=-1, limit=None, skip=0):
        #     """
        #     查询传入条件集合和全部数据
        #     :return:
        #     """
        #     # cursor = collection.find().sort('i').limit(1000).skip(2)
        #     # cursor = db.test_collection.find({'i': {'$lt': 5}}).sort('i')
        #     # for document in cursor.to_list(length=None):
        #     #     pprint.pprint(document)
        #     #
        #     # return collection.find().sort('i')
        #     cursor = collection.find()
        #     # cursor.sort('i', sort).skip(skip).limit(limit)  # 排序将消耗巨大性能所以不建议在大批量导出的情况下进行排序
        #     cursor.skip(skip).limit(limit)
        #     # for document in cursor.to_list(length=100):
        #     #     pprint.pprint(document)
        #
        #     # for document in cursor:
        #     #     pprint.pprint(document)
        #
        #     return cursor.to_list(length=None)

    def find_col(self, *args, **kwargs):
        """查找某一列数据

        :param args: 某些字段，如"name","age"
        :param kwargs: 某些字段匹配，如gender="male"
        :return:
        """
        key_dict = {"_id": 0}  # 不显示_id
        key_dict.update({i: 1 for i in args})
        return [i for i in self.collection.find(kwargs, key_dict)]

    def insert_one(self, **kwargs):
        """
        单条插入
        :param kwargs:
        :return:
        """
        try:
            result = self.collection.insert_one(kwargs)
            print('inserted_id %s' % repr(result.inserted_id))
            return 'ok'
        except Exception as e:
            return str(e)

    def find_one(self, args, kwargs):
        """
        按条件查询单个doc,如果传入集合为空将返回默认数据
        :param args: 指定字段显示
        :param kwargs:  查询条件
        :return:
        """
        result_obj = self.collection.find_one(args, kwargs)
        return result_obj

    def find_conditions(self, limit=0, **kwargs):
        """
        按条件查询，并做返回条数限制
        :param limit:
        :param kwargs:
        :return:
        """
        # return collection.find(kwargs).limit(limit)
        if limit == 0:
            # cursor = collection.find(kwargs).sort('i').skip(0)
            cursor = self.collection.find(kwargs).skip(0)
        else:
            cursor = self.collection.find(kwargs).sort('i').limit(limit).skip(0)
        return cursor.to_list(length=None)

# print(PyMongoUtil().count())
# print(PyMongoUtil().find_all())
