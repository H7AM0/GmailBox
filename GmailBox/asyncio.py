
import re
import pytz
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)
from pypasser import reCaptchaV3
from bs4 import BeautifulSoup
from urllib.parse import unquote
from typing import Optional, List
from .my_types import new_emailResult,inboxResult
from .async_session import make_request,session_manager


__all__ = ["GmailBox"]


class GmailBox:
    def __init__(self):
        self.headers = {
            'Pragma': 'no-cache',
            'Accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        self.code = None
        self.session = None
        self.rapidapi = None
        self.key = None
        self.gmail = None
        self.timestamp = 0

    async def new_email(self) -> "new_emailResult":
        reCaptcha_response = reCaptchaV3('https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Ldd8-IUAAAAAIdqbOociFKyeBGFsp3nNUM_6_SC&co=aHR0cHM6Ly9zbWFpbHByby5jb206NDQz&hl=ar&v=vjbW55W42X033PfTdVf6Ft4q&size=invisible&cb=vikeanpgkmyu')
        r = await make_request('https://smailpro.com/temp-gmail', method='get', headers=self.headers, response_type='cookies')
        self.headers["x-xsrf-token"] = unquote(r['XSRF-TOKEN'])
        self.headers["x-g-token"] = reCaptcha_response
        if not self.rapidapi:
            req = await make_request('https://smailpro.com/js/chunks/smailpro_v2_email.js', method='get', headers=self.headers, response_type='text')
            self.rapidapi = req.split('rapidapi_key:"')[1].split('"')[0]
        if not self.key:
            json_data = {
                'domain': 'gmail.com',
                'username': 'random',
                'server': 'server-1',
                'type': 'alias',
            }
            response = await make_request('https://smailpro.com/app/key', method='post', headers=self.headers, json=json_data, response_type='json')
            self.key = response['items']

        req = await make_request(f'https://public-sonjj.p.rapidapi.com/email/gm/get?key={self.key}&rapidapi-key={self.rapidapi}&domain=gmail.com&username=random&server=server-1&type=alias', method='get', headers=self.headers, response_type='json')
        self.email = req['items']['email']
        self.timestamp = req['items']['timestamp']
        return new_emailResult.parse(self.email)

    async def inbox(self, email: Optional[str] = None, limit: int = None) -> List[inboxResult]:  
        reCaptcha_response = reCaptchaV3('https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Ldd8-IUAAAAAIdqbOociFKyeBGFsp3nNUM_6_SC&co=aHR0cHM6Ly9zbWFpbHByby5jb206NDQz&hl=ar&v=vjbW55W42X033PfTdVf6Ft4q&size=invisible&cb=vikeanpgkmyu')
        r = await make_request('https://smailpro.com/temp-gmail', method='get', headers=self.headers, response_type='cookies')
        self.headers["x-xsrf-token"] = unquote(r['XSRF-TOKEN'])
        self.headers["x-g-token"] = reCaptcha_response
        email = email or self.email
        json_data = {
            "email": email,
            "timestamp": self.timestamp
        }
        response = await make_request('https://smailpro.com/app/key', method='post', headers=self.headers, json=json_data, response_type='json')
        self.key = response['items']
        response = await make_request(f'https://api.sonjj.com/email/gm/check?key={self.key}&rapidapi-key={self.rapidapi}&email={email}&timestamp={self.timestamp}', method='get', headers=self.headers, response_type='json')
        messages = []
        for item in response["items"]:
            if limit is not None and len(messages) == limit:
                break
            message_id = item['mid']
            sender = item['textFrom']
            subject = item['textSubject']
            target_time_str = item['textDate']
            utc_plus_7_tz = pytz.timezone('Asia/Bangkok')
            utc_plus_7_time = datetime.now(utc_plus_7_tz)
            target_time = datetime.strptime(target_time_str, '%Y-%m-%d %H:%M:%S')
            target_time = utc_plus_7_tz.localize(target_time)
            time_difference =  utc_plus_7_time - target_time
            time_difference_in_minutes = time_difference.total_seconds() / 60
            time = "{:.0f}".format(time_difference_in_minutes)
            if time == "1" or time == "0":
                time = "1 minute ago"
            else:
                time = f"{time} minutes ago"
            json_data = {
                'email': f'{email}',
                'message_id': f'{message_id}',
            }
            
            response = await make_request('https://smailpro.com/app/key', method='post', headers=self.headers, json=json_data, response_type='json')
            self.key = response['items']
            response = await make_request(f'https://api.sonjj.com/email/gm/read?key={self.key}&email={email}&message_id={message_id}', method='get', headers=self.headers, response_type='json')
            html = response['items']['body']
            cleaned_html_content = re.sub(r'\\/', '/', html)
            soup = BeautifulSoup(cleaned_html_content, 'html.parser')
            message = soup.text.strip()
            messages.append(inboxResult.parse({
                'sender': sender,
                'html': cleaned_html_content,
                'subject': subject,
                'message': message,
                'time': time
            }))
        return messages

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        session = await session_manager.get_session()
        await session.close()
