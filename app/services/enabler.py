import importlib
import logging
from typing import List

from entities import Job, Schedule


class ZeroJobsToEnableException(Exception):
    pass


class Enabler:
    '''Create jobs instances based on yaml configuration'''

    def __init__(self, job_object_list: List[dict]) -> None:
        self._job_object_list: List[dict] = []
        self.log = logging.getLogger()
        self.source_path = 'jobs'
        self._jobs: List[Job] = []
        self._register_jobs(job_object_list)

    def _register_jobs(self, job_object_list):
        for job in job_object_list:
            self._job_object_list.append(job)
            self.log.debug(f'registering new job: {job}')

    @property
    def jobs(self) -> List[Job]:
        return self._jobs

    def enable_jobs(self):
        for job_dict in self._job_object_list:
            if job_dict.get('active', True):
                job = self.__create_instance(job_dict)
                if job != None:
                    self._jobs.append(job)
        if len(self._jobs) > 0:
            self.log.debug(f'{len(self._jobs)} jobs were enabled')
        else:
            self.log.fatal('zero jobs to enable')
            raise ZeroJobsToEnableException

    def __create_instance(self, job_dict: dict) -> Job | None:
        '''dynamically create job instance'''
        try:
            classname: str = job_dict.get('name')
            schedule = job_dict.get('schedule')
            priority = job_dict.get('priority', 0)

            mod = importlib.import_module(
                name=f'.{classname}', package=f'.{self.source_path}')
            _class = getattr(mod, self.__to_camel_case(classname))

            job: Job = _class()
            job.priority = priority
            interval = schedule.get('interval')
            time_unit = schedule.get('time_unit', 's')
            delay = schedule.get('delay', 0)

            _schedule = Schedule(interval=interval, time_unit=time_unit, delay=delay)

            job.schedule = _schedule

            return job
        except Exception as e:
            self.log.error(e.args[0])
            return

    def __to_camel_case(self, class_name: str) -> str:
        return ''.join(word.title() for word in class_name.split('_'))
