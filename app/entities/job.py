from uuid import UUID, uuid4

from .schedule import Schedule

class Job:
    def __init__(self) -> None:
        self.id: UUID = uuid4()
        self.schedule: Schedule = None

    def execute(self):
        '''execute the job'''

    def __repr__(self) -> str:
        return f'Job(id={self.id}, schedule={self.schedule})'
