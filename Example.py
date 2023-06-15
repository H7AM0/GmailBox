import sys,time
def jalan(z):
    for e in z + '\n':
        sys.stdout.write(e)
        sys.stdout.flush()
        time.sleep(00000.009)

logo = '\n\n\n\n\t\t░░░░░▄▄▀▀▀▀▀▀▀▀▀▄▄░░░░░\n\t\t░░░░█░░░░░░░░░░░░░█░░░░\n\t\t░░░█░░░░░░░░░░▄▄▄░░█░░░\n\t\t░░░█░░▄▄▄░░▄░░███░░█░░░\n\t\t░░░▄█░▄░░░▀▀▀░░░▄░█▄░░░\n\t\t░░░█░░▀█▀█▀█▀█▀█▀░░█░░░\n\t\t░░░▄██▄▄▀▀▀▀▀▀▀▄▄██▄░░░\n\t\t░▄█░█▀▀█▀▀▀█▀▀▀█▀▀█░█▄░'
jalan(logo)
jalan('\x1b[1;36m \t\t░░░╔╗╔╗╔══╗╔═╦═╗╔═╗░░░░░░░░\n\t\t░░░║╚╝║║╔╗║║║║║║║║║░░░░░░░░\n\t\t░░░║╔╗║║╠╣║║║║║║║║║░░░░░░░░\n\t\t░░░╚╝╚╝╚╝╚╝╚╩═╩╝╚═╝░░░░░░░░\n\n\n')
####################################
##### pip install GmailBox==0.0.1
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