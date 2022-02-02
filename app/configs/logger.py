import logging


class Logger:
    def __init__(self) -> None:
        log_level = logging.INFO
        format = '%(asctime)s - %(name)s - %(process)d - %(module)s.%(funcName)s::%(lineno)s - %(levelname)s - %(message)s'
        datetime_format = '%d-%b-%y %H:%M:%S'
        formatter = logging.Formatter(format, datetime_format)
        logger = logging.getLogger()
        logger.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
