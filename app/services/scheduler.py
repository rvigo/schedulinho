import asyncio
import logging
from datetime import datetime, timedelta
from typing import List

from entities import Job


class NoJobsToRunException(Exception):
    pass


class Scheduler:
    def __init__(self) -> None:
        self.log = logging.getLogger()
        self.jobs: List[Job] = []
        self.runnables: List[Job] = []
        self._priority = {}

    def schedule(self, jobs: List[Job]) -> None:
        [self.jobs.append(self._schedule_first_run(job))
         for job in jobs]

    def _schedule_first_run(self, job: Job) -> Job:
        now = datetime.now()
        job.last_run = now.replace(microsecond=0)
        job.next_run = job.last_run + timedelta(seconds=job.delay)
        self.log.info(f'next run in {str(job.next_run)}')
        return job

    def prepare_to_run(self) -> None:
        self.runnables.clear()

        for job in self.jobs:
            if self._should_run(job):
                self.runnables.append(job)
                self._schedule_last_and_next_run(job)

        if len(self.runnables) > 0:
            self.log.debug(f'{len(self.runnables)} runnables jobs')
        else:
            raise NoJobsToRunException

    async def run(self) -> List[tuple]:
        return await asyncio.gather(*[job.execute() for job in self.runnables])

    def _schedule_last_and_next_run(self, job: Job) -> Job:
        now = datetime.now()
        job.last_run = now.replace(microsecond=0)
        job.next_run = job.last_run + timedelta(seconds=job.schedule)
        self.log.info(f'next run in {str(job.next_run)}')
        return job

    def _should_run(self, job: Job) -> bool:
        return datetime.now() >= job.next_run
