from GmailBox import GmailBox
from prettytable import PrettyTable

# ░░░░░▄▄▀▀▀▀▀▀▀▀▀▄▄░░░░░
# ░░░░█░░░░░░░░░░░░░█░░░░
# ░░░█░░░░░░░░░░▄▄▄░░█░░░
# ░░░█░░▄▄▄░░▄░░███░░█░░░
# ░░░▄█░▄░░░▀▀▀░░░▄░█▄░░░
# ░░░█░░▀█▀█▀█▀█▀█▀░░█░░░
# ░░░▄██▄▄▀▀▀▀▀▀▀▄▄██▄░░░
# ░▄█░█▀▀█▀▀▀█▀▀▀█▀▀█░█▄░
# ░░░╔╗╔╗╔══╗╔═╦═╗╔═╗░░░░ Author : Mohamed Ahmed Amer | Hamo
# ░░░║╚╝║║╔╗║║║║║║║║║░░░░ Github : https://github.com/H7AM0
# ░░░║╔╗║║╠╣║║║║║║║║║░░░░ Telegram : https://t.me/hamo_back
# ░░░╚╝╚╝╚╝╚╝╚╩═╩╝╚═╝░░░░ Instagram : https://instagram.com/4.4cq/''')

# Create a random Gmail and receive messages


def set_number_in_middle(text, num_lines):
    half = num_lines // 2
    if num_lines % 2 == 0:
        result = '\n' * half + text + '\n' * (half-1)
    else:
        result = '\n' * half + text + '\n' * half
    return result

def split_text(text, num_words):
    words = text.split()
    return '\n'.join([' '.join(words[i:i+num_words]) for i in range(0, len(words), num_words)])

def create_or_select_email():
    while True:
        choice = input('''
[ 1 ] Create a new email.
[ 2 ] Use a previously created email.
Please choose 1 or 2: ''')

        if choice == '1':
            new_email = Gmail.new_email()
            email = new_email['email']
            print(f'\n[ * ] Your email: {email}\n')
            return email
        elif choice == '2':
            email = input('\n[ ? ] Enter Email: ')
            print()
            return email
        else:
            print("\n[ ! ] Please choose 1 or 2 only.")

def display_inbox(email):
    print("\n[ ? ] Press enter to check your inbox.")
    input()
    inbox = Gmail.inbox(email)

    if inbox:
        table = PrettyTable(["#", "Time", "From", "Email", "Subject"])
        
        for index, item in enumerate(inbox):
            from_, email, subject, time = item['from'], item['email'], item['subject'], item['time']
            email, from_, time, subject = map(lambda x: split_text(x, 1), [email, from_, time, subject])
            table.add_row([set_number_in_middle(str(index), len(subject.split('\n'))), time, from_, email, subject])
            table.add_row(['-', '-----', '-----', '-----', '-----'])
        table.del_row(-1)
        print(table)
        all_inbox_len = len(inbox) - 1
        
        while True:
            message_index = input(f'\n[ ? ] Choose a message number (0 to {all_inbox_len}) to view: ')
            
            if message_index.isdigit():
                message_index = int(message_index)
                
                if 0 <= message_index <= all_inbox_len:
                    message = inbox[message_index]['message']
                    print(f'\n{message}\n')
                    break
                else:
                    print(f"\n[ ! ] Please choose a number from 0 to {all_inbox_len}.\n")
            else:
                print("\n[ ! ] Please enter a valid number to display a message.\n")

        input('[ ? ] Press enter to view another message.')
        display_inbox(email)
    else:
        print("\n[ ! ] No messages in your inbox.")
        display_inbox(email)

Gmail = GmailBox()
email = create_or_select_email()
display_inbox(email)
