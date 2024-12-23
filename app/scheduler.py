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


# Indices
async def tge_indices_scrape_job():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://0.0.0.0:8000/indices/save")
        logger.info(f"TGE Indices scrape job executed at {datetime.now()}, status code: {response.status_code}")

# WAHP
async def tge_wahp_scrape_job():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://0.0.0.0:8000/tge-wahp/save")
        logger.info(f"TGE WAHP scrape job executed at {datetime.now()}, status code: {response.status_code}")

# Hour contracts
async def tge_hour_contracts_scrape_job():
    async with httpx.AsyncClient() as client:
        logger.info(f"@@@@@@@@@@@@@@@@@@ WORKS @@@@@@@@@@@@@@@@@@@@")
        response = await client.post("http://0.0.0.0:8000/tge-rdn/tge-rdn")
        logger.info(f"TGE Hour Contracts scrape job executed at {datetime.now()}, status code: {response.status_code}")

# Block contracts
async def tge_block_contracts_scrape_job():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://0.0.0.0:8000/block-contracts/save")
        logger.info(f"TGE block contracts scrape job executed at {datetime.now()}, status code: {response.status_code}")

async def debug_job():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://0.0.0.0:8000/tge-rdn/check")
        logger.info(f"Check at {datetime.now()}, status code: {response.status_code}")

def start_scheduler():
    scheduler = BackgroundScheduler()

    # TGE Indices 10:52 AM/PM
    scheduler.add_job(lambda: asyncio.run(tge_indices_scrape_job()), 'cron', hour=10, minute=52,
                      id='Morning TGE indices scrape')
    scheduler.add_job(lambda: asyncio.run(tge_indices_scrape_job()), 'cron', hour=22, minute=52,
                      id='Evening TGE indices scrape')

    # TGE WAHP 10:53 AM/PM
    scheduler.add_job(lambda: asyncio.run(tge_wahp_scrape_job()), 'cron', hour=10, minute=53,
                      id='Morning TGE WAHP scrape')
    scheduler.add_job(lambda: asyncio.run(tge_wahp_scrape_job()), 'cron', hour=22, minute=53,
                      id='Evening TGE WAHP scrape')

    # TGE Hour Contracts 10:54 AM/PM
    scheduler.add_job(lambda: asyncio.run(tge_hour_contracts_scrape_job()), 'cron', hour=10, minute=54,
                      id='Morning TGE hour contracts scrape')
    scheduler.add_job(lambda: asyncio.run(tge_hour_contracts_scrape_job()), 'cron', hour=22, minute=54,
                      id='Evening TGE hour contracts scrape')

    # TGE Block Contracts 10:55 AM/PM
    scheduler.add_job(lambda: asyncio.run(tge_hour_contracts_scrape_job()), 'cron', hour=10, minute=55,
                      id='Morning TGE block contracts scrape')
    scheduler.add_job(lambda: asyncio.run(tge_hour_contracts_scrape_job()), 'cron', hour=22, minute=55,
                      id='Evening TGE hour_contracts scrape')

    scheduler.start()
