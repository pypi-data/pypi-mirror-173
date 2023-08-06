from .notification_mode import NotificationMode
from .message_property import MessageProperty

class NotificationServiceRequest:

    def __init__(self):
        self._source_system = None
        self._timestamp = None
        self._message_id = None
        self._message_type = None
        self._priority = None
        self._message = None
        self._schedule_time = None
        self._message_properties = None
        self._notification_modes = []
        self._owner = None
        self._logurl = None

    @property
    def owner(self) -> str:
        return self._owner
    
    @owner.setter
    def owner(self, owner: str):
        self._owner = owner
    
    @property
    def logurl(self) -> str:
        return self._logurl

    @logurl.setter
    def logurl(self, logurl: str):
        self._logurl = logurl
    
    @property
    def source_system(self) -> str:
        return self._source_system
    
    @source_system.setter
    def source_system(self, source_system: str):
        self._source_system = source_system

    @property
    def timestamp(self) -> str:
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, timestamp: str):
        self._timestamp = timestamp

    @property
    def message_id(self) -> str:
        return self._message_id
    
    @message_id.setter
    def message_id(self, message_id: str):
        self._message_id = message_id
    
    @property
    def message_type(self) -> str:
        return self._message_type
    
    @message_type.setter
    def message_type(self, message_type: str):
        self._message_type = message_type

    @property
    def priority(self) -> str:
        return self._priority
    
    @priority.setter
    def priority(self, priority: str):
        self._priority = priority
    
    @property
    def message(self) -> str:
        return self._message
    
    @message.setter
    def message(self, message: str):
        self._message = message

    @property
    def schedule_time(self) -> str:
        return self._schedule_time
    
    @schedule_time.setter
    def schedule_time(self, schedule_time: str):
        self._schedule_time = schedule_time
    

    @property
    def message_properties(self) -> MessageProperty:
        return self._message_properties
    
    @message_properties.setter
    def message_properties(self, message_properties: MessageProperty):
        self._message_properties = message_properties
    
    @property
    def notification_modes(self):
        return self._notification_modes
    
    @notification_modes.setter
    def notification_modes(self, notification_modes: NotificationMode):
        self._notification_modes = notification_modes

    