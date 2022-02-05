import logging
from datetime import date, datetime

from entities import Job
from utils.asyncfy import asyncfy


class Example(Job):
    def __init__(self) -> None:
        super().__init__()
        self.log = logging.getLogger()

    @asyncfy
    def execute(self):

        self.log.info(datetime.now())
