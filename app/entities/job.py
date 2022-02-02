from datetime import datetime


class Job:
    def __init__(self) -> None:
        self.schedule: int = 0
        self.last_run: datetime = None
        self.next_run: datetime = None
        self.priority: int = 0
        self.delay: int = 0

    def execute(self):
        '''execute the job'''
