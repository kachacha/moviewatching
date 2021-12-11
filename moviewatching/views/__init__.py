from flask_restx import Api

from .search_api import api as search

api = Api(
    title='zfeno - 影视纵览',
    version='1.0',
    description='zfeno - 影视纵览 API',
    doc='/debug/'
)

api.add_namespace(search, path='/zfeno-video/api/v1')
