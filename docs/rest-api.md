# 爬虫翻译工具接口文档

![作者](https://img.shields.io/badge/作者-张峰-brightgreen)
![版本](https://img.shields.io/badge/版本-v1.0.0-orange)

版本：v1.1.0

线下调试接口地址：`http://192.168.1.252:5000`

线上测试接口地址：`http://scoring-system.edge.zylliondata.local`

线上正式接口地址：`http://scoring-system.apps.zylliondata.local`

## 语言翻译接口

功能说明：此功能提供两种任意语言相互转换的功能，此功能为网络在线翻译爬取，不可做并发量测试。

`POST`:`/dsg/api/v1/login`

#### Headers 参数

```json
{
  "Content-Type": "multipart/form-data",
  "Authorization": "****"
}
```

|参数|是否必要|类型|内容|描述|
|:---:|:---:|:---:|:---:|:---:|
|Content-Type|True|String|multipart/form-data|数据类型|

#### Body 参数

```text
        get_parser.add_argument('keyword', type=str, help='输入关键词', required=True, default='')
        get_parser.add_argument('from', type=str, help='原语言', required=False, default='auto')
        get_parser.add_argument('to', type=str, help='翻译成语言', required=True, default='en')
        get_parser.add_argument('bing_', type=str, help='必应翻译', required=False, default=False)
        get_parser.add_argument('baidu_', type=str, help='百度翻译', required=False, default=False)
keyword:*keyword*
from:*from*
to:*to*
bing_:*bing_*
baidu_:*baidu_*
```

|参数|是否必要|类型|内容|描述|
|:---:|:---:|:---:|:---:|:---:|
| keyword | True | String |  | 翻译关键词 |
| from | False | String |  | 原语言/默认自动识别 |
| to | True | String |  | 需转换语言/en（英语）、fa（日语） |
| bing_ | False | Bool |  | Bing 翻译开关/默认关闭 |
| baidu_ | False | Bool |  | Baidu 翻译开关/默认关闭 |

#### 返回示例

状态码：200

```json
{
  "message": "successful crawl news.",
  "get_translate_data": {
    "bing__json": [
      {
        "detectedLanguage": {
          "language": "zh-Hans",
          "score": 1
        },
        "translations": [
          {
            "text": "Data quality-related articles",
            "to": "en"
          }
        ]
      }
    ]
  }
}
```

#### 错误列表

|状态码|内容|描述|
|:---:|:---:|:---:|
|400|`{"message": "请检查你的关键词信息！"}`|参数注册|
|400|`{"message": "内部错误！"}`|系统错误|
