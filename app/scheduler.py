from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

import os
import sys
import httpx
import asyncio

import logging

logger = logging.getLogger(__name__)

if os.getenv('LOGGING_LEVEL') == 'debug':
    level = logging.DEBUG
else:
    level = logging.INFO

logging.basicConfig(level=level,
                    format='%(levelname)s:     %(asctime)s     %(name)s     %(message)s',
                    stream=sys.stdout)

async def scrape_job():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://0.0.0.0:8000/tge-rdn/tge-rdn")
        logger.info(f"Scrape job executed at {datetime.now()}, status code: {response.status_code}")

async def debug_job():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://0.0.0.0:8000/tge-rdn/check")
        logger.info(f"Check at {datetime.now()}, status code: {response.status_code}")

def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(lambda: asyncio.run(scrape_job()), 'cron', hour=10, minute=55, id='Morning scrape')
    scheduler.add_job(lambda: asyncio.run(scrape_job()), 'cron', hour=22, minute=55, id='Evening scrape')

    scheduler.start()
