import re
from bs4 import BeautifulSoup
from urllib.parse import unquote
from typing import Optional, List
from.types import new_emailResult,inboxResult
import asyncio
from .async_session import make_request,session_manager


__all__ = ["GmailBox"]


class GmailBox:
    def __init__(self):
        self.headers = {
            'Pragma': 'no-cache',
            'Accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        self.token = None
        self.email = ""

    async def new_email(self) -> "new_emailResult":
        req = await make_request('https://www.emailnator.com/', method='get', headers=self.headers, response_type='cookies')
        self.token = unquote(req['XSRF-TOKEN'])
        self.headers["x-xsrf-token"] = self.token
        json_data = {'email': ['dotGmail']}
        response = await make_request('https://www.emailnator.com/generate-email', method='post', headers=self.headers, json=json_data, response_type='json')
        self.email = response['email'][0]
        return new_emailResult.parse(self.email)

    async def inbox(self, email: Optional[str] = None, limit: int = None) -> List[inboxResult]:  
        req = await make_request('https://www.emailnator.com/', method='get', headers=self.headers, response_type='cookies')
        self.token = unquote(req['XSRF-TOKEN'])
        self.headers["x-xsrf-token"] = self.token
        email = email or self.email
        await asyncio.sleep(0.5)
        json_data = {'email': email}
        response = await make_request('https://www.emailnator.com/message-list', method='post', headers=self.headers, json=json_data, response_type='json')
        
        messages = []
        for item in response.get('messageData', [])[1:]:
            if limit is not None and len(messages) == limit:
                break
            messageID = item['messageID']
            json_data = {'email': email, 'messageID': messageID}
            response = await make_request('https://www.emailnator.com/message-list', method='post', headers=self.headers, json=json_data, response_type='text')
            soup = BeautifulSoup(response, 'html.parser')
            message = soup.text.strip()
            try:
                time_part, message = re.search(r"Time:\s*\n\s*\n(.+?)([\s\S]+)", message).groups()
            except AttributeError:
                time_part = "Unknown"
            
            sender = item['from']
            messages.append(inboxResult.parse({
                'sender': sender,
                'html': response,
                'subject': item['subject'],
                'message': message.strip(),
                'time': item.get('time', time_part)
            }))
        return messages

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        session = await session_manager.get_session()
        await session.close()
