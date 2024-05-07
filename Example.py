
####################################
## Author : Mohamed Ahmed Amer | Hamo
## Github : https://github.com/H7AM0
## Telegram : https://t.me/hamo_back
## Instagram : https://instagram.com/4.4cq/
####################################
##### pip install GmailBox==0.0.6
####################################

from GmailBox import GmailBox


Gmail = GmailBox()
New_Gmail = Gmail.newEmail()
email = New_Gmail['email']
print(f' [*] your email : {email}')

def box():
    print()
    input(" [?] Press enter to inbox : ")
    print()
    inbox = Gmail.inbox(email)
    if inbox:
        for hamo in inbox:
            print("======================")
            print(f" [#] received sinceone {hamo['time']}")
            print(f" [#] from : {hamo['from']} <{hamo['email']}>")
            print(f" [#] subject : {hamo['subject']}")
            print("----------------------------------")
            print(f" {hamo['message']}")
        print()
        box()
    else:
        box()

box()