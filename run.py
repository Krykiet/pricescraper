import uvicorn

from app.config import get_config

import logging
import os
import sys

config = get_config()

if os.getenv('LOGGING_LEVEL') == 'debug':
    level = logging.DEBUG
else:
    level = logging.INFO

logger = logging.getLogger(__name__)

logging.basicConfig(level=level,
                    format='%(levelname)s:     %(asctime)s     %(name)s     %(message)s',
                    stream=sys.stdout)

if __name__ == "__main__":

    if config.local:
        logger.info("@@ Config: local @@")
        uvicorn.run("app.main:app", host='0.0.0.0', port=8000, reload=config.local)
    elif config.prod:
        logger.info("@@ Config: prod @@")
        uvicorn.run("app.main:app", port=10000, host='0.0.0.0', reload=config.prod)
    elif config.remote:
        logger.info("@@ Config: remote @@")
        uvicorn.run("app.main:app", host='0.0.0.0', port=8000)

