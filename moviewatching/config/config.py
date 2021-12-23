import os


class Base:
    APP_NAME = '影视纵览（Film And Television Overview）'
    SECRET_KEY = "Film And Television Overview"


class Development(Base):
    MONGODB_USERNAME = None
    MONGODB_PASSWORD = None
    MONGODB_URI = "mongodb://127.0.0.1:27017/"
    MONGODB_PORT = 27017
    MONGODB_DB = "VideoPlus"
    MONGODB_TABLE_VIDEO_INFO = "video_info"
    MONGODB_TABLE_ANALYSIS_URI = "analysis_uri"
    MONGODB_TABLE_PAGE = "page"


class Production(Base):
    MONGODB_USERNAME = os.environ.get("MONGODB_DB", "zfeno")
    MONGODB_PASSWORD = os.environ.get("MONGODB_DB", "jiehuai.qing")
    MONGODB_URI = os.environ.get("MONGO_URI",
                                 "mongodb://{0}:{1}@49.234.34.225:27017/".format(MONGODB_USERNAME, MONGODB_PASSWORD))
    MONGODB_PORT = int(os.environ.get("MONGODB_PORT", 27017))
    MONGODB_DB = os.environ.get("MONGODB_DB", "VideoPlus")
    MONGODB_TABLE_VIDEO_INFO = os.environ.get("MONGODB_TABLE_VIDEO_INFO", "video_info")
    MONGODB_TABLE_ANALYSIS_URI = os.environ.get("MONGODB_TABLE_ANALYSIS_URI", "analysis_uri")
    MONGODB_TABLE_PAGE = os.environ.get("MONGODB_TABLE_PAGE", "page")


if __name__ == '__main__':
    aaa = [
        # {"name": "解析1", "url": "https://api.sigujx.com/jx/?url=", "selected": True},
        {'name': 1, "url": "http://okjx.cc/?url=", "selected": True},
        {"name": 2, "url": "https://www.administratorw.com/video.php?url=", "selected": True},
        {"name": 3, "url": "https://jx.618g.com/?url=", "selected": True},
        {"name": 4, "url": "http://17kyun.com/api.php?url=", "selected": True},
        {"name": 5, "url": "https://jx.ejiafarm.com/dy.php?url=", "selected": True},
        {"name": 6, "url": "https://www.8090.la/8090/?url=", "selected": True}
    ]
    from pymongo import MongoClient

    client = MongoClient("mongodb://zfeno:jiehuai.qing@49.234.34.225:27017/")
    db = client["VideoPlus"]  # 数据库
    collection = db["analysis_uri"]  # 表
    print(collection.find_one({"id": 123}))
    # for one in aaa:
    #     save = {
    #         "id": one["name"],
    #         "uri": one["url"],
    #         "selected": True
    #     }
    #     print(save)
    #     collection.insert_one(save)
