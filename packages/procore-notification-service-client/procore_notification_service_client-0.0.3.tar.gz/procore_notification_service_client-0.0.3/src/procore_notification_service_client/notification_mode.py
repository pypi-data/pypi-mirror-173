import json
from enum import Enum
from re import L, template

class NotificationModeItem(Enum):
    SLACK = "Slack"
    SMS = "SMS"
    EMAIL = "EMAIL"

class NotificationMode:

    def __init__(self):
        self._mode = None
        self._template_name = None
        self._slack_channel = None
        self._phone_number = None
        self._emails = None

    @property
    def mode(self) -> NotificationModeItem:
        return self._mode
    
    @mode.setter
    def mode(self, mode: NotificationModeItem):
        self._mode = mode
    

    @property
    def template_name(self) -> str:
        return self._template_name

    @template_name.setter
    def template_name(self, template_name: str):
        self._template_name = template_name

    @property
    def slack_channel(self) -> str:
        return self._slack_channel

    @slack_channel.setter
    def slack_channel(self, slack_channel: str):
        self._slack_channel = slack_channel

    @property
    def phone_number(self) -> int:
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number: int):
        self._phone_number = phone_number


    @property
    def emails(self) -> str:
        return self._emails

    @emails.setter
    def emails(self, emails: str):
        self._emails = emails

    
    def __str__(self):
        return  f"""{
            "mode": {self.mode},
            "Template_name": {self.template_name},            
            "Slack_channel": {self.slack_channel},
            "phone_number": {self.phone_number},
            "Emails": {self.emails}
        }"""

    

    

