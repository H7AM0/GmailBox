# GmailBox

> With this library, you can create random Gmail and receive messages

## Install :
```commandline
pip install -U GmailBox
```
## How to use?
- Here an example to use it:
```python
from GmailBox import GmailBox

Gmail = GmailBox()

# Create a new gmail
New_Gmail = Gmail.new_email()
email = New_Gmail.email
print(email)

# Start checking the inbox
inbox = Gmail.inbox(email)

# If there are messages in the inbox, print them
if inbox:
    for message in inbox:
        print("=" * 21)
        print(message)
    print("=" * 21)
# If no messages were received, print a message
else:
    print(f' [!] No messages were received.')

```
- Here an async example:
```python
from GmailBox.asyncio import GmailBox
import asyncio

# Define the main function
async def main():
    Gmail = GmailBox()

    # Create a new gmail
    New_Gmail = await Gmail.new_email()
    email = New_Gmail.email
    print(email)
    
    # Start checking the inbox
    inbox = await Gmail.inbox(email)

    # If there are messages in the inbox, print them
    if inbox:
        for message in inbox:
            print("=" * 21)
            print(message)
        print("=" * 21)
    # If no messages were received, print a message
    else:
        print(f' [!] No messages were received.')

# Run the main function
asyncio.run(main())
```
## On Pypi
* <a href="https://pypi.org/project/GmailBox">GmailBox</a>
## Author
<p align="center">
    <a href="https://github.com/H7AM0/GmailBox">
        <img src="https://telegra.ph/file/19f7cbbf3959941cda6b5.jpg" alt="Hamo" width="128">
    </a>
    <br>
    <b>Hamo • حـمــو</b>
    <br>
    <a href="https://www.instagram.com/4.4cq/">
        Instagram <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram" width="20">
    </a>
    • 
    <a href="https://t.me/hamo_back">
        <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" alt="Telegram" width="20"> Telegram
    </a>
</p>

