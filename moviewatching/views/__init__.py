from flask_restx import Api

from .analysis_api import api as analysis
from .episode_api import api as episode
from .search_api import api as search

api = Api(
    title='zfeno - 影视纵览',
    version='1.0',
    description='zfeno - 影视纵览 API',
    doc='/debug/'
)

api.add_namespace(search, path='/zfeno-video/api/v1')
api.add_namespace(episode, path='/zfeno-video/api/v1')
api.add_namespace(analysis, path='/zfeno-video/api/v1')
