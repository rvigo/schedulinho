from typing import List
import logging
import yaml
import os
from pathlib import Path
from entities.job import Job


class NoConfigurationFileFound(Exception):
    pass


class Loader:
    def __init__(self) -> None:
        self.log = logging.getLogger()
        self.config = {}
        try:
            self.config['jobs'] = []
            files = os.listdir('/app/jobs/configuration_files')
            for file in files:
                path = Path(file)
                if '.yml' == path.suffix or '.yaml' == path.suffix:
                    with open(f'/app/jobs/configuration_files/{path.name}') as f:
                        job_config: dict = yaml.load(f, Loader=yaml.FullLoader)
                        self.config['jobs'].append(
                            {k: v for k, v in job_config['job'].items()})

        except FileNotFoundError:
            self.log.critical('no configuration file found!')
            raise NoConfigurationFileFound

    @property
    def jobs(self) -> List[Job]:
        return self.config['jobs']
