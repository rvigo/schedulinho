from datetime import datetime, timedelta
from croniter import croniter


class Schedule:
    TIME_UNIT_MAP = [('s', 'seconds'),
                     ('m', 'minutes'),
                     ('h', 'hours'),
                     ('d', 'days'),
                     ('c', 'cron')]
    TIME_UNIT_CONVERSION_MAP = {'s': 1,
                                'm': 60,
                                'h': 3600,
                                'd': 86400}

    def __init__(self, interval, time_unit, delay) -> None:
        self.interval = interval
        self.time_unit: str = time_unit[0] if any(
            time_unit in _tuple for _tuple in self.TIME_UNIT_MAP) else 's'

        if self.time_unit == 'c':
            self.cron = croniter(
                self.interval, datetime.now(), ret_type=datetime)
            delta: timedelta = self.cron.get_current() - datetime.now()
            self.delay = delta.total_seconds()
        else:
            self.delay = delay
        self.last_run: datetime = datetime.now()
        self.next_run: datetime = datetime.now()

    @property
    def offset(self) -> int:
        if self.time_unit == 'c':
            return self.cron.next(ret_type=float) - self.cron.get_prev(ret_type=float)
        return self.TIME_UNIT_CONVERSION_MAP[self.time_unit] * self.interval

    def __repr__(self) -> str:
        return f'Schedule(interval={self.interval}, time_unit={self.time_unit}, delay={self.delay})'
