import yagmail
import keyring


def sendemail(subj, body):
    keyring.set_password('yagmail', 'aus.pcparts1@gmail.com', '301Bobby')
    receiver = "andyapp106@gmail.com"
    yag = yagmail.SMTP("aus.pcparts1@gmail.com")
    yag.send(
    to=receiver,
    subject=subj,
    contents=body,
    )