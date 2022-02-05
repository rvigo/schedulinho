from datetime import datetime


class Schedule:
    TIME_UNIT_MAP = [('s', 'seconds'), ('m', 'minutes'),
                     ('h', 'hours'), ('d', 'days')]
    TIME_UNIT_CONVERSION_MAP = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}

    def __init__(self, interval, time_unit, delay) -> None:
        self.interval = interval
        self.time_unit: str = time_unit[0] if any(
            time_unit in _tuple for _tuple in self.TIME_UNIT_MAP) else 's'

        # delay = in seconds
        self.delay = delay
        self.last_run: datetime = None
        self.next_run: datetime = None

    @property
    def offset(self) -> int:
        return self.TIME_UNIT_CONVERSION_MAP[self.time_unit] * self.interval

    def __repr__(self) -> str:
        return f'Schedule(interval={self.interval}, time_unit={self.time_unit}, delay={self.delay})'
