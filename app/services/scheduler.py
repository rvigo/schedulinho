import asyncio
from datetime import datetime, timedelta
import logging
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
        job.schedule.last_run = now.replace(microsecond=0)
        job.schedule.next_run = job.schedule.last_run + \
            timedelta(seconds=job.schedule.delay)
        self.log.info(
            f'job: {job.__class__.__name__} - next run in {str(job.schedule.next_run)}')
        return job

    def prepare_to_run(self) -> None:
        self.runnables.clear()

        for job in self.jobs:
            if self._should_run(job):
                self.runnables.append(job)
                self._schedule_next_run(job)

        if len(self.runnables) > 0:
            self.log.debug(f'{len(self.runnables)} runnables jobs')
        else:
            raise NoJobsToRunException

    async def run(self):
        await asyncio.gather(*[job.execute() for job in self.runnables])

    def _schedule_next_run(self, job: Job) -> Job:
        now = datetime.now()
        job.schedule.last_run = now.replace(microsecond=0)
        job.schedule.next_run = job.schedule.last_run + \
            timedelta(seconds=job.schedule.offset)
        self.log.info(
            f'job: {job.__class__.__name__} - next run in {str(job.schedule.next_run)}')
        return job

    def _should_run(self, job: Job) -> bool:
        return datetime.now() >= job.schedule.next_run
