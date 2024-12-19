import uvicorn

import logging
import os
import sys

if os.getenv('LOGGING_LEVEL') == 'debug':
    level = logging.DEBUG
else:
    level = logging.INFO

logger = logging.getLogger(__name__)

logging.basicConfig(level=level,
                    format='%(levelname)s:     %(asctime)s     %(name)s     %(message)s',
                    stream=sys.stdout)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host='0.0.0.0', port=8000, reload=True)

