import time,re
import requests
from bs4 import BeautifulSoup

class GmailBox:
    def __init__(self):
        self.request = requests.session()
        headers = {
            'authority': 'www.emailnator.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        self.request.get('https://www.emailnator.com/', headers=headers)
        token = str(self.request.cookies.get_dict()['XSRF-TOKEN'][:-3])+str("=")
        self.token = token
    def newEmail(self):
        headers = {
            'authority': 'www.emailnator.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'origin': 'https://www.emailnator.com',
            'referer': 'https://www.emailnator.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': f'{self.token}',
        }

        json_data = {
            'email': [
                'plusGmail',
                'dotGmail',
            ],
        }

        response = self.request.post('https://www.emailnator.com/generate-email', headers=headers, json=json_data).json()
        email = response['email'][0]
        return {'email':email}
    def inbox(self,email):
        time.sleep(0.20) 
        headers = {
            'authority': 'www.emailnator.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'origin': 'https://www.emailnator.com',
            'referer': 'https://www.emailnator.com/inbox/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': f'{self.token}',
        }

        json_data = {
            'email': f'{email}',
        }

        response = self.request.post('https://www.emailnator.com/message-list', headers=headers, json=json_data).json()
        hamo = []
        for index,item in enumerate(response['messageData']):
            if index == 0:
                continue
            hamo.append(item)
        end = []
        for hamoo in hamo:
            messageID = hamoo['messageID']
            headers = {
                 'authority': 'www.emailnator.com',
                 'accept': 'application/json, text/plain, */*',
                 'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
                 'content-type': 'application/json',
                'origin': 'https://www.emailnator.com',
                'referer': f'https://www.emailnator.com/inbox/{email}/{messageID}',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'x-xsrf-token': f'{self.token}',
            }

            json_data = {
                'email': f'{email}',
                'messageID': f'{messageID}',
            }

            text = self.request.post('https://www.emailnator.com/message-list', headers=headers, json=json_data).text
            soup = BeautifulSoup(text, 'html.parser')
            sender = hamoo['from']
            emaill = re.findall(r'<(.*?)>', sender)[0]
            sender = re.findall(r'"(.*?)"', sender)[0]
            subject = hamoo['subject']
            timee = hamoo['time']
            message = '\n'.join([p.text for p in soup.find_all('p')])
            end.append({'from':sender,'email':emaill,'subject':subject,'message':message,'time':timee})
        return end
