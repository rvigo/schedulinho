from .schedule import Schedule


class Job:
    def __init__(self) -> None:
        self.schedule: Schedule = None
        self.priority: int = 0

    def execute(self):
        '''execute the job'''

    def __repr__(self) -> str:
        return f'Job(schedule={self.schedule}, priority={self.priority})'
