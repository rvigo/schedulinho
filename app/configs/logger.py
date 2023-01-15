import logging
import os

from .discord_handler import DiscordFilter, DiscordHandler


class Logger:
    def __init__(self) -> None:
        log_level = os.getenv('SCHED_LOG_LEVEL', logging.INFO)
        format = '%(asctime)s - %(module)s.%(funcName)s::%(lineno)s - %(levelname)s - %(message)s'
        datetime_format = '%d-%b-%y %H:%M:%S'
        formatter = logging.Formatter(format, datetime_format)
        logger = logging.getLogger()
        logger.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        discordHandler = DiscordHandler()
        discordFilter = DiscordFilter()
        discordHandler.addFilter(discordFilter)
        logger.addHandler(handler)
        logger.addHandler(discordHandler)
