__version__ = "0.0.9"

import time
import re
from bs4 import BeautifulSoup
from urllib.parse import unquote
from typing import Optional, List

from .types import new_emailResult, inboxResult
from .session import make_request

__all__ = ["GmailBox"]

class GmailBox:
    def __init__(self):
        self.headers = {
            'Pragma': 'no-cache',
            'Accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        self.email = ""

    def new_email(self) -> new_emailResult:
        req = make_request('https://www.emailnator.com/', method='get', headers=self.headers, response_type='cookies')
        self.token = unquote(req['XSRF-TOKEN'])
        self.headers["x-xsrf-token"] = self.token
        json_data = {'email': ['dotGmail']}
        response = make_request('https://www.emailnator.com/generate-email', method='post', headers=self.headers, json=json_data, response_type='json')
        self.email = response['email'][0]
        return new_emailResult.parse(self.email)

    def inbox(self, email: Optional[str] = None, limit: int = None) -> List[inboxResult]:
        req = make_request('https://www.emailnator.com/', method='get', headers=self.headers, response_type='cookies')
        self.token = unquote(req['XSRF-TOKEN'])
        self.headers["x-xsrf-token"] = self.token
        email = email or self.email
        time.sleep(0.5)
        json_data = {'email': email}
        response = make_request('https://www.emailnator.com/message-list', method='post', headers=self.headers, json=json_data, response_type='json')
        messages = []
        for item in response['messageData'][1:]:  
            if limit is not None and len(messages) == limit:
                break
            messageID = item['messageID']
            json_data = {'email': email, 'messageID': messageID}
            response = make_request('https://www.emailnator.com/message-list', method='post', headers=self.headers, json=json_data, response_type='text')
            soup = BeautifulSoup(response, 'html.parser')
            message = soup.text.strip()
            try:
                tim, message = re.search(r"Time:\s*\n\s*\n(.+?)([\s\S]+)", message).groups()
            except:
                tim = None
            sender = item['from']
            messages.append(inboxResult.parse({
                'sender': sender,
                'html': response,
                'subject': item['subject'],
                'message': message.strip(),
                'time': item.get('time', tim)
            }))
        return messages

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self
