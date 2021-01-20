import yagmail
import keyring


def sendemail(subj,body):
    keyring.set_password('yagmail', 'sender email', 'pw')
    receiver = "receiver email"
    yag = yagmail.SMTP("sender email")
    yag.send(
    to=receiver,
    subject=subj,
    contents=body, 
    )   
