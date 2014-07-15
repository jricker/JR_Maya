import email
import smtplib
def sendEmail():
    msg = email.mime.Multipart.MIMEMultipart()
    msg['Subject'] = 'Render Email Test'
    msg['From'] = ''
    msg['To'] = ''
    password = ''

    body = email.mime.Text.MIMEText("""
        here is where we test out the email body text
        """)
    msg.attach(body)
    # send via Gmail server
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    #
    print 'FINISHED SENDING Email HOPEFULLY'
sendEmail()