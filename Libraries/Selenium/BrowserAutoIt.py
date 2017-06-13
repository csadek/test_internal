import autoit
from time import sleep


class BrowserAutoIt(object):

    @staticmethod
    def login(window_name, username, password):
        print "Waiting for window with name: " + window_name
        autoit.win_wait(window_name, 30)
        if not autoit.win_exists(window_name):
            raise Exception("No Browser Login Window is found")
        else:
            print "Activating window"
            autoit.win_activate(window_name)
            sleep(1)
            print "Sending username & password"
            autoit.send(username)
            autoit.send("{tab}")
            autoit.send(password)
            autoit.send("{enter}")

    @staticmethod
    def file_upload(window_name, file_name):
        autoit.win_wait(window_name, 30)
        if not autoit.win_exists(window_name):
            raise Exception("No File Upload Window is found")
        else:
            autoit.win_activate(window_name)
            autoit.control_focus(window_name, "[ID:1148]")
            autoit.control_set_text(window_name, "[ID:1148]", file_name)
            autoit.control_click(window_name, "[ID:1]")
