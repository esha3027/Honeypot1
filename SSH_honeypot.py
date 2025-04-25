# Libraries
import logging
from logging.handlers import RotatingFileHandler
import socket, paramiko, threading

# Constants
logging_format = logging.Formatter('%(message)s')
SSH_BANNER = "SSH-2.0-MySSHServer_1.0"

# Host_key
host_key = paramiko.RSAKey(filename = 'server.key')

# Loggers and Logging Files
funnel_logger = logging.getLogger('FunnelLogger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler('audits.log', maxBytes = 2000, backupCount = 5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

creds_logger = logging.getLogger('CredsLogger')
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler('cmdaudits.log', maxBytes = 2000, backupCount = 5)
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler)

# Emulated Shell
def emulated_shell(channel, client_IP):
    channel.send(b'corporate-jumpbox2$')
    command = b""
    while True:
        char = channel.recv(1)
        channel.send(char)
        if not char:
            channel.close()
        command += char
        if char == b'\r':
            if command.strip() == b'exit':
                response = b'\n GoodBye! \n'
                channel.close()
            elif command .strip() == b'pwd':
                response = b"\n" +b'\\user\\local' +b'\r\n'
                creds_logger.info(f'Command {command.strip()}' + 'executed by' + f'{client_IP}')
            elif command.strip() == b'whoami':
                response = b"\n" + b"User20" + b"\r\n"
                creds_logger.info(f'Command {command.strip()}' + 'executed by' + f'{client_IP}')
            elif command.strip() == b'ls':
                response = b'\n' + b"jumpbox1.conf" + b"\r\n"
                creds_logger.info(f'Command {command.strip()}' + 'executed by' + f'{client_IP}')
            elif command.strip() == b'cat jumpbox1.conf':
                response = b'\n' + b"Go to deeboodah.com" + b"\r\n"
                creds_logger.info(f'Command {command.strip()}' + 'executed by' + f'{client_IP}')
            else:
                response = b'\n' + bytes(command.strip()) + b"\r\n"
                creds_logger.info(f'Command {command.strip()}' + 'executed by' + f'{client_IP}')

            channel.send(response)
            channel.send(b'corporate-jumpbox2$')
            command = b""

# SSH Server + Sockets
class SSH_Server(paramiko.ServerInterface):
    def __init__(self, client_IP, input_username=None, input_password=None):
        self.event = threading.Event()
        self.client_IP = client_IP
        self.input_username = input_username
        self.input_password = input_password
    def check_channel_request(self, kind, chanid: int) -> int:
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
    def get_allowed_auths(self, *args):
        return "password"
    def check_auth_password(self, username, password):
        funnel_logger.info(f'Client {self.client_IP} attempted connection with' + f'username: {username},' + f'password: {password}.')
        creds_logger.info(f'{self.client_IP}, {username}, {password}.')
        if self.input_username is not None and self.input_password is not None:
            if username == self.input_username and password == self.input_password:
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
        else:
            return paramiko.AUTH_SUCCESSFUL
    def check_channel_shell_request(self, channel):
        self.event.set()
        return True
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    def check_channel_exec_request(self, channel, command):
        command = str(command)
        return True

def client_handle(client, addr, username, password):
    client_IP = addr[0]
    print(f"{client_IP} has connected to the server.")
    try:
        transport = paramiko.Transport(client)
        transport.local_version = SSH_BANNER
        server = SSH_Server(client_IP = client_IP, input_username = username, input_password = password)
        
        transport.add_server_key(host_key)

        transport.start_server(server = server)
        
        channel = transport.accept(100)
        if channel is None:
            print("No channel was opened.")
        
        standard_banner = "Welcome to the New Session!!\r\n\r\n"
        channel.send(standard_banner)
        emulated_shell(channel, client_IP = client_IP)

    except Exception as error:
        print(error)
        print("!!!ERROR!!!")
    finally:
        try:
            transport.close()
        except Exception as error:
            print(error)
            print("!!!ERROR!!!")
        client.close()
        

# Provision SSh-based Honeypot
def honeypot(address, port, username,password):
    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socks.bind((address, port))
    
    socks.listen(100)
    print(f"SSH server is listening on port {port}.")
    
    while True:
        try:
            client, addr = socks.accept()
            ssh_honeypot_thread = threading.Thread(target = client_handle, args = (client, addr, username, password))
            ssh_honeypot_thread.start()
        except Exception as error:
            print(error)
