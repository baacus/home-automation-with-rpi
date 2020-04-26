from get_emails import GetEmail
from os import system, chmod
from time import sleep
from datetime import datetime

class IFTTTListener:
    @property
    def task_list(self):
        return self._task
    @task_list.setter
    def task_list(self, value):
        self._task = value
     
    def __init__(self, email, pwd, subj, path):
        self.gmail_obj = GetEmail("imap.gmail.com", email, pwd)
        self.conn = self.gmail_obj.connect()
        self.subject = subj
        self._task = None
        self.path = path
        self.__write_config()

    def __check_cancelling(self):
        try:
            with open(self.path + "/" + 'config.txt', 'r') as f:
                line = f.readline().replace(" ", "").replace("\n","").lower()
                if line == "cancel:1":
                    with open(self.path + "/" + 'log.txt', 'a+') as a:
                        a.write("\r\nIFTTT Listener is cancelled on {}".format(datetime.now().strftime("%d-%m-%Y,%H:%M")))
                    return True
        except:
            pass
        return False
    def __write_config(self):
        try:
            with open(self.path + "/" + 'config.txt', 'w') as w:
                w.write("cancel:0")
            chmod(self.path + "/" + 'config.txt',0o777)
        except:
            pass
    
    def get_event(self):
        res, _, sbj, body = self.gmail_obj.read_unseen()
        message = ""
        if res:
            if sbj == self.subject:
                body = body.split('\r\n\r\n')
                message = body[1]
            else:
                res = False
        return res, message
    
    def do_action(self, action):
        system(action)
    
    def do_tasks(self, sleep_time = 2):
        first_attempt = True
        while True:
            sleep(sleep_time)
            cancel = self.__check_cancelling()
            if cancel:
                print("IFTTT Listener is cancelled")
                break
            if not self.conn:
                print("Connection could not be established")
                self.conn = self.gmail_obj.connect()
                continue
            
            if first_attempt:
                print("Connection is established. Checking for new events...")
                first_attempt = False
            
            if type(self._task) != dict:
                raise NotImplementedError("Task_List is not a dictionary!")
            
            check, msg = self.get_event()
            if not check:
                continue
            
            if msg not in self._task:
                print("Not defined event: {}".format(msg))
                continue
            
            try:
                print("New event found: {}".format(msg))
                self.do_action(self._task[msg])
            except:
                print("Some error occured while executing the command")
            

    


