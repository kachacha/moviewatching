import os


class Base:
    APP_NAME = '影视纵览（Film And Television Overview）'
    SECRET_KEY = "Film And Television Overview"


class Development(Base):
    MONGO_URI = "mongodb://127.0.0.1:27017/"
    # REDIS_HOST = 'localhost'
    # MONGODB_HOST = "172.25.2.33"
    MONGODB_PORT = 27017
    MONGODB_DB = "VideoPlus"
    MONGODB_TABLE_ANALYSIS_URI = "analysis_uri"
    MONGODB_TABLE_PAGE = "page"


class Production(Base):
    REDIS_HOSTS = os.environ.get('REDIS_HOSTS', '172.25.2.25,172.25.2.26,172.25.2.27')
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://172.25.2.31:27017,172.25.2.31:27017,172.25.2.33:27017")
    MONGODB_HOST = os.environ.get("MONGODB_HOST", "172.25.2.33")
    MONGODB_PORT = int(os.environ.get("MONGODB_PORT", 27017))
    MONGODB_DB = os.environ.get("MONGODB_DB", "iDSG")
    MONGODB_TABLE = os.environ.get("MONGODB_TABLE", "task")
    MONGODB_TABLE_USER = os.environ.get("MONGODB_TABLE_USER", "user")
    MONGODB_TABLE_WEBSITE = os.environ.get("MONGODB_TABLE_WEBSITE", "website_data")

    PAGING = int(os.environ.get("PAGING", 9))  # 领取任务列表分页数量
    TOTAL_PAGE = int(os.environ.get("TOTAL_PAGE", 21))  # 需要搜索 gitlab 中的总页数
    SCORE_NUMBER = int(os.environ.get("SCORE_NUMBER", 4))  # 每个 spider 需要评分的数量

    CREAT_PROJECT = "http://team-cooperation.apps.zylliondata.local/api/v1/gitlab/create"  # gitlab 创建项目链接
    URL_BUILDER_API = "http://url-builder.edge.zylliondata.local/api/v1/crawl/url-builder"  # 构造链接请求


if __name__ == '__main__':
    aaa = [
        # {"name": "解析1", "url": "https://api.sigujx.com/jx/?url=", "selected": True},
        # {'name': "解析2", "url": "http://okjx.cc/?url=", "selected": True},
        {"name": 2, "url": "https://www.administratorw.com/video.php?url=", "selected": True},
        {"name": 3, "url": "https://jx.618g.com/?url=", "selected": True},
        {"name": 4, "url": "http://17kyun.com/api.php?url=", "selected": True},
        {"name": 5, "url": "https://jx.ejiafarm.com/dy.php?url=", "selected": True},
        {"name": 6, "url": "https://www.8090.la/8090/?url=", "selected": True}
    ]
    from pymongo import MongoClient

    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client["VideoPlus"]  # 数据库
    collection = db["analysis_uri"]  # 表
    for one in aaa:
        save = {
            "id": one["name"],
            "uri": one["url"],
            "selected": True
        }
        print(save)
        collection.insert_one(save)
