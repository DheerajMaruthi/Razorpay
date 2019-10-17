import threading
from django.core.mail import EmailMultiAlternatives


class EmailThread(threading.Thread):
    def __init__(self, body, from_email, to, cc):
        self.body = body
        self.from_email = from_email
        self.to = to
        self.cc = cc
        threading.Thread.__init__(self)

    def run(self):
        email_object = EmailMultiAlternatives(subject='KIMS-CSR Donation',
                                              from_email=self.from_email,
                                              to=[self.to],
                                              cc=self.cc)
        email_object.attach_alternative(self.body, "text/html")
        email_object.send()
