from time import sleep
import paramiko


class SourceCopyLibrary(object):

    def __init__(self):
        print ("Starting Initialization ...")
        self.initial_wait = 5
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Check SSH connection method
    def verify_connection(self, ip, username, password, trials=10, wait=30):
        print ("Starting connection check with IP: {}, username: {} & Password: {} ...".format(ip, username, password))
        sleep(self.initial_wait)
        while trials != 0:
            try:
                print ("Trying to connect to: " + ip)
                self.ssh.connect(ip, 22, username, password)
                print ("Connection is available ...")
                self.ssh.close()
                print ("Connection is verified successfully ...")
                return
            except Exception as e:
                print ("Connection not available yet due to exception: " + str(e))
                print ("Remaining trials: " + str(trials))
                sleep(wait)
            trials -= 1
        raise Exception("SSH Connection could not be established.")
