####################################
## Author : Mohamed Ahmed Amer | Hamo
## Github : https://github.com/H7AM0
## Telegram : https://t.me/hamo_back
## Instagram : https://instagram.com/4.4cq/
####################################
##### pip install GmailBox==0.0.9
####################################

from GmailBox import GmailBox

def check_inbox(Gmail, email):
    """Check and display emails in the inbox recursively."""
    print(f' [*] Your email: {email}')
    input(" [?] Press Enter to check inbox: ")
    
    # Fetch inbox messages for the given email
    inbox = Gmail.inbox(email)
    
    if inbox:
        for message in inbox:
            print("=" * 21)
            print(message)
        print("=" * 21)
        
        # Recursively check the inbox again
        check_inbox(Gmail, email)
    else:
        print(f' [!] No messages were received.')
        print("=" * 21)
        
        # Recursively check the inbox again
        check_inbox(Gmail, email)

def main():
    """Main function to initialize GmailBox and start checking the inbox."""
    Gmail = GmailBox()
    
    # Create a new email
    New_Gmail = Gmail.new_email()
    email = New_Gmail.email
    
    # Start checking the inbox
    check_inbox(Gmail, email)

# Entry point of the script
if __name__ == "__main__":
    main()
