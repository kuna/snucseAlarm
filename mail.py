#
# sends email to user
#

# get receiver's addr: private.email
import private

import smtplib
from email.mime.text import MIMEText

# default value
email_from = "noreply@noreply.com"

def createEmail(article):
    msg = MIMEText(article['detail'])
    msg['Subject'] = article['title']
    msg['To'] = private.email
    msg['From'] = email_from
    return msg

def emailArticle(article):
    msg = createEmail(article)
    s = smtplib.SMTP('localhost')
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    s.quit()

def emailArticles(articles):
    for article in articles:
        emailArticle(article)
