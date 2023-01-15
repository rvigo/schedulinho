from logging import Filter, LogRecord, StreamHandler
import os

from discord_webhook import DiscordEmbed, DiscordWebhook


class DiscordHandler(StreamHandler):
    def __init__(self) -> None:
        super().__init__()
        self.discord = Discord()

    def emit(self, record: LogRecord):
        job_name = record.__dict__.get('job_name', None)
        icon_url = record.__dict__.get('icon_url', None)
        log_level = record.__dict__.get('levelname', None)

        message = self.format(record)
        self.discord.send(message, job_name, icon_url, log_level)


class DiscordFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        return 'discord' in record.__dict__


class Discord:
    LOG_LEVEL_COLOR = {'INFO': '03B2F8',
                       'WARNING': 'FFD700',
                       'ERROR': 'FF1100'}

    def __init__(self) -> None:
        self.webhook_url = os.environ.get('DISCORD_WEBHOOK')
        self.webhook = DiscordWebhook(url=self.webhook_url)

    def send(self, message: str, job_name: str = None, icon_url: str = None, log_level='INFO'):
        if job_name and icon_url:
            print(f'icon url is: {icon_url}')
            embed = DiscordEmbed(description=message,
                                 color=self.LOG_LEVEL_COLOR.get(log_level, 'INFO'))

            embed.set_author(name=job_name,
                             icon_url=icon_url)

            self.webhook.add_embed(embed)
        else:
            self.webhook.content = message

        self.webhook.execute(remove_embeds=True)
        self.webhook.content = None
