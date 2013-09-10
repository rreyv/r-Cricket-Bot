import smtplib
from email.mime.text import MIMEText


def sendEmail(subject,text):
	message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (fromUser, ",".join(toUser), subject, text)
	try:
		s = smtplib.SMTP('smtp.gmail.com', 587)
	 	s.ehlo()
	 	s.starttls()
	 	s.ehlo()
	 	s.login(fromUser,fromPass)
	 	s.sendmail(fromUser, toUser, message)
	 	s.quit()
	except:
	 	print "Error, couldn't send email. Might be gmail is down."