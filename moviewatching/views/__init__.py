from flask_restplus import Api

from .translate_api import api as translate

api = Api(
    title='zfeno - 影视纵览',
    version='1.0',
    description='zfeno - 影视纵览 API',
    doc='/debug/'
)

api.add_namespace(translate, path='/idsg/api/v1')
