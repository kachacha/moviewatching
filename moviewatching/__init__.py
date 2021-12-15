__author__ = "张峰"
__copyright__ = "© 2016-2018 中云开源技术（上海）有限公司保留一切权利。"
__version__ = "v1.0"
__maintainer__ = "zhangf"
__email__ = "zhangf@zylliondata.com"
__status__ = "Development"
__date__ = "2019-09-23"

from flask import Flask, render_template
from flask_cors import CORS

from .config.config import Development, Production


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'super secret string'

    if test_config:
        app.config.from_object(Development)
    elif app.debug:
        app.config.from_object(Development)
    else:
        app.config.from_object(Production)

    CORS(app, supports_credentials=True)

    @app.route('/')
    def version():
        return 'Search Engine Dashboard 1.0'

    @app.route('/welcome')
    def health():
        return render_template("welcome.jinja2")

    from .views import api
    api.init_app(app)

    return app
