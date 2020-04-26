import email
import imaplib
import os

class GetEmail:
    def __init__(self, serv, addr, pwd):
        self.server = serv
        self.address = addr
        self.password = pwd
        self.mail = None
    
    def connect(self):
        result = False
        try:
            self.mail = imaplib.IMAP4_SSL(self.server)
            self.mail.login(self.address, self.password)
            result = True
        except:
            pass
        return result
    def read_unseen(self):
        result = False
        email_obj = [None,"","",""]
        try:
            self.mail.select("inbox")
            _ , data = self.mail.uid('search', None, '(UNSEEN)')
            inbox_item_list = data[0].split()
            oldest = inbox_item_list[0]
            _ , email_data = self.mail.uid('fetch', oldest, '(RFC822)')
            raw_email = email_data[0][1].decode("UTF-8")
            email_message = email.message_from_string(raw_email)

            if email_message.is_multipart():
                email_obj[1] = email_message["From"]
                email_obj[2] = email_message["Subject"]
                for part in email_message.walk():
                    if (part.get_content_type() == 'text/plain') and (part.get('Content-Disposition') is None):
                        #body part
                        email_obj[3] = part.get_payload()
                result = True
        except IndexError:
            pass
        except Exception as e:
            print("Some error occured")
            print(e)
        finally:
            email_obj[0] = result
            return tuple(email_obj)
