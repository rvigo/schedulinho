import asyncio
import logging
import time

from configs import Logger
from services import Enabler, Loader, Scheduler
from services.enabler import ZeroJobsToEnableException
from services.loader import NoConfigurationFileFound
from services.scheduler import NoJobsToRunException

Logger()
log = logging.getLogger()

async def main():
    try:
        loader = Loader()
        enabler = Enabler(loader.jobs)
        enabler.enable_jobs()
        scheduler = Scheduler()
        scheduler.schedule(enabler.jobs)
        while True:
            try:
                await scheduler.run()
                log.info('waiting for next run')
            except NoJobsToRunException:
                pass
            finally:
                time.sleep(1)
    except (ZeroJobsToEnableException, NoConfigurationFileFound):
        return


if __name__ == '__main__':
    loop = asyncio.run(main())
    log.debug('shutting down')
