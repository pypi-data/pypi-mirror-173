from paramiko import SSHClient
from getpass import getpass
import time


class HPC:
    def __init__(self, hostname = 'login1.gbar.dtu.dk') -> None:
        # Connect
        self.client = SSHClient()
        self.client.load_system_host_keys()
        username = input("Username: ")
        pw = getpass("Password: ")
        self.client.connect(hostname, username=username, password=pw)
    

    def shell(self):
        # open channel
        channel = self.client.get_transport().open_session()
        channel.get_pty()
        channel.invoke_shell()

        # read welcome message
        time.sleep(1)
        while not channel.recv_ready():
            print("Working...")
            time.sleep(2)
        print(channel.recv(4096).decode("utf-8"))

        # interactive commands
        while True:
            # get command
            command = input('$ ')

            # exit
            if command == 'exit':
                break
            
            # send command
            channel.send(command + "\n")
            time.sleep(.1)

            # read output
            while not channel.recv_ready():
                print("Working...")
                time.sleep(2)
            out = channel.recv(1024).decode("utf-8")
            out = "\n".join(out.split("\n")[1:-2])
            print(out)
        
        # close connection
        self.close()

    def close(self):
        self.client.close()


if __name__ == "__main__":
    HPC().shell()