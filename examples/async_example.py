####################################
## Author : Mohamed Ahmed Amer | Hamo
## Github : https://github.com/H7AM0
## Telegram : https://t.me/hamo_back
## Instagram : https://instagram.com/4.4cq/
####################################
##### pip install GmailBox==1.0.0
####################################

import asyncio
from GmailBox.asyncio import GmailBox

async def check_inbox(Gmail, email):
    """Asynchronously check and display emails in the inbox recursively."""
    print(f' [*] Your email: {email}')
    input(" [?] Press Enter to check inbox: ")
    
    # Fetch inbox messages asynchronously for the given email
    inbox = await Gmail.inbox(email)
    
    if inbox:
        for message in inbox:
            print("=" * 21)
            print(message)
        print("=" * 21)
        
        # Recursively check the inbox again
        await check_inbox(Gmail, email)
    else:
        print(f' [!] No messages were received.')
        print("=" * 21)
        
        # Recursively check the inbox again
        await check_inbox(Gmail, email)

async def main():
    """Main function to initialize GmailBox and start checking the inbox asynchronously."""
    async with GmailBox() as Gmail:
        # Create a new email asynchronously
        New_Gmail = await Gmail.new_email()
        email = New_Gmail.email
        
        # Start checking the inbox
        await check_inbox(Gmail, email)

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())
