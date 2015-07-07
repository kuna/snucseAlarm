#
# sends email to user
#

# get receiver's addr: private.email
import private

# gmail
import yagmail
from email.mime.text import MIMEText

def createEmail(article):
    #msg = MIMEText(article['detail'])
    msg = {}
    msg['Body'] = article['detail']
    msg['Subject'] = article['title']
    msg['To'] = private.gmail_id
    msg['From'] = private.gmail_id
    return msg

def emailArticle(article):
    msg = createEmail(article)
    yag = yagmail.SMTP(private.gmail_id, private.gmail_password)
    yag.send(to=msg['To'], subject=msg['Subject'], contents=msg['Body'])

def emailArticles(articles):
    for article in articles:
        emailArticle(article)

#test
#emailArticle({'detail':'this is a test', 'title':'test'})
