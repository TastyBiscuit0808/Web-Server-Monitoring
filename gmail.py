import smtplib
from email.message import EmailMessage


def email_alert(subject, body, to):


    sender_email = "---"
    sender_password = "---"
    reciever_mail = to
    subject = "Alert!! Webserver might be down!!"
    mail_body = body

    message = f"From: {sender_email}\nTo: {reciever_mail}\nSubject: {subject}\n\n{body}"

    with smtplib.SMTP('smtp.gmail.com',587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, reciever_mail, message)

# if __name__ == '__main__':
#     email_alert("Test", "https://discord.gg/cAWW5qq", "3095824273@vtext.com")