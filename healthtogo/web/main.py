import os
import logging

from .server import create_app


def main_app(test_config=None):
    return create_app(test_config)


if __name__ == '__main__':
    logging.info("Running from main.py\n")
    app = main_app()
    port = int(app.config.get('HTTP_PORT', os.environ.get("HTTP_PORT", "5050")))
    debug = bool(app.config.get('debug', 'false'))

    app.run(host='0.0.0.0', threaded=True, debug=debug, port=port)  # nosec: B104
