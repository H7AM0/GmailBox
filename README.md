<p align="center">
    <a href="https://github.com/H7AM0/GmailBox">
        <img src="https://telegra.ph/file/d3d163f7a0de39e8ce7da.mp4" alt="Hamo" width="128">
    </a>
    <br>
    <b>Hamo • حـمــو</b>
    <br>
    <a href="https://www.instagram.com/4.4cq/">
        Instagram
    </a>
     • 
    <a href="https://t.me/hamo_back">
        Telegram
    </a>
</p>

# GmailBox

> With this library, you can create random Gmail and receive messages

``` python
from GmailBox import GmailBox

Gmail = GmailBox()
```
## Generate a random Gmail
``` python
New_Gmail = Gmail.newEmail()
print(New_Gmail)
```
## to get the inbox
``` python
email = New_Gmail['email']
inbox = Gmail.inbox(email)
print(inbox)
```
### Installing

``` bash
pip3 install GmailBox
```
### On Pypi
* <a href="https://pypi.org/project/GmailBox">GmailBox</a>
