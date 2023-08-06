"""
Uses slack sdk for post message on channel
"""

import logging

from decouple import config
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)


class SlackNotify:
    """
    A class for uses the slack sdk to send a message
    """

    def __init__(self, app_name: str) -> None:
        self.app_name = app_name
        self.client = self.connect()

    def connect(self):
        """
        Return a webclient instance
        """
        return WebClient(token=config("SLACK_BOT_TOKEN"))

    def get_channel_by_is_error(self, is_error: bool):
        return config("SLACK_BOT_ERRORS_CHANNEL") if is_error else config("SLACK_BOT_REPORTS_CHANNEL")

    def make_text(self, message):
        return f"[{self.app_name}]: {message}"

    def notify(self, message: str, is_error: bool = False, emit_log: bool = False):
        """
        Method to notify a message and post it into a channel
        """
        channel = self.get_channel_by_is_error(is_error=is_error)
        text = self.make_text(message)
        try:
            self.client.chat_postMessage(channel=channel, text=text)
            if emit_log:
                if is_error:
                    logger.error(text)
                else:
                    logger.info(text)
        except SlackApiError as exc:
            assert exc.response["ok"] is False
            assert exc.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            error = exc.response["error"]
            logger.error("Got an error: {error}", error=error)
        except Exception as exc:
            logger.error("An Exception occurred {exc}", exc=exc)
