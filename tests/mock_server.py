from flask import Flask

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def create_app():
    app = Flask(__name__)

    # register mock modules
    from .mockEndpoints import group_mocks
    from .mockEndpoints import login_mocks
    from .mockEndpoints import file_mocks
    from .mockEndpoints import registration_mocks
    app.register_blueprint(group_mocks.api_bp)
    app.register_blueprint(login_mocks.api_bp)
    app.register_blueprint(file_mocks.api_bp)
    app.register_blueprint(registration_mocks.api_bp)

    return app
