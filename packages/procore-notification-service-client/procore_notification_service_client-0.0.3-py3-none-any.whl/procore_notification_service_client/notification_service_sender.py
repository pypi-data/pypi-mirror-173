from pkg_resources import empty_provider
import collections.abc
import urllib3
import urllib.parse
import base64
import json
from datetime import datetime 
from json import JSONEncoder
import os

from .message_property import MessageProperty
from .notification_mode import NotificationMode, NotificationModeItem
from .notification_service_request import NotificationServiceRequest

class NotificationServiceEncoder(JSONEncoder):
    def default(self, obj):        
        if isinstance(obj, MessageProperty):        
            return { "property1": obj.property1, "property2": obj.property2 }
        elif type(obj).__name__ == 'NotificationMode':
            result = {}
            result['mode']  = obj.mode.value
            result['Template_name'] = obj.template_name
            if obj.mode == NotificationModeItem.EMAIL:
                result['Emails'] = obj.emails
            elif obj.mode == NotificationModeItem.SMS:
                result['phone_number'] = obj.phone_number
            elif obj.mode == NotificationModeItem.SLACK:
                result['Slack_channel'] = obj.slack_channel
            return result
        else:
            return super().default(obj)

class NotificationServiceSender:
    
    def __init__(self, url):
        self.url = url
        self.authenticate_token = None
        self._is_authenticate = False
        
        
    @property
    def is_authenticate(self):
        return self._is_authenticate
    
    @is_authenticate.setter
    def is_authenticate(self, is_authenticate):
        self._is_authenticate = is_authenticate
        

    #    This method authenticates to the AWS Cognito Pool in order
    #    to get the token to later on will be using to send Request to 
    #    Moniker
    def authenticate_and_get_token(self,
                notification_auth_url: str,                
                app_client_id: str, app_client_secret: str) -> None:
        
        header_token = f'{app_client_id}:{app_client_secret}'.encode('ascii')
        base64_token = base64.b64encode(header_token).decode("utf-8")    
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {base64_token}'};    
        data = {'grant_type': 'client_credentials', 
                'scope': 'com.procore.moniker.notification/write'}      
        data = urllib.parse.urlencode(data)
        http = urllib3.PoolManager()
        r = http.request('POST', notification_auth_url,
                body=data, headers=headers, retries=False)                    
        if r.status == 200:
            self.authenticate_token = json.loads(r.data)['access_token']                      
            self._is_authenticate = True
            print("Log in success")                    
        else:            
            print("Error on login")               


    '''
        this method sends the request to the Notification Service.
    '''
    def process_notification(self, notification_request: NotificationServiceRequest):
        time = datetime.now()        
        token = self.authenticate_token  
        endpoint_url = f'{self.url}'   
        environment = 'stg'
        if os.environ.get('environment') is not None:
            environment = os.environ.get('environment')
        headers = {'Content-type': 'application/json', 'Authorization': token}
        data = {}
        data['source_system'] = notification_request.source_system
        data['timestamp'] = notification_request.timestamp
        data['message_id'] = notification_request.message_id
        data['message_type'] = notification_request.message_type
        data['priority'] = notification_request.priority
        data['message'] = notification_request.message
        data['schedule_time'] = notification_request.schedule_time
        data['message_properties'] = notification_request.message_properties
        data['notification_modes'] = notification_request.notification_modes

        #Those fields are optional
        if notification_request.owner is not None:            
            data['owner'] = notification_request.owner
        
        if notification_request.logurl is not None:
            data['logurl'] = notification_request.logurl

        #data = {'source_system': notification_request.source_system, 
        #        'timestamp': notification_request.timestamp,
        #        'message_id': notification_request.message_id, 
        #        'message_type': notification_request.message_type, 
        #        'priority': notification_request.priority,
        #        'message': notification_request.message,
        #        "schedule_time": notification_request.schedule_time,
        #        'message_properties': notification_request.message_properties,
        #        'notification_modes': notification_request.notification_modes
        #        }    
        try:
            http = urllib3.PoolManager()
            notification_request = json.dumps(data, cls=NotificationServiceEncoder)
            print(f'Notification Request: {notification_request}')
            r = http.request('POST', endpoint_url, body=notification_request, headers=headers, retries=False)
            site_response = str(r.data.decode('utf-8'))                        
            print(f'Notification Response: {site_response}')
            return notification_request, site_response
        except Exception as err:
            print(err)
            return notification_request, None

                