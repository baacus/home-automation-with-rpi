from sys import path

_path = "/home/pi/Documents/ifttt"
path.insert(1, _path)

from ifttt import IFTTTListener

def main():

    obj = IFTTTListener("your.account@gmail.com", "your_password","IFTTT_Request",_path)
    obj.task_list = {
        "on":  "sudo uhubctl -l 1-1 -p 2 -a 1",
        "off": "sudo uhubctl -l 1-1 -p 2 -a 0"
    }

    obj.do_tasks(sleep_time=2)

if __name__ == "__main__":
    main()