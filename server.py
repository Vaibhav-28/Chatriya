import socket
import threading

HOST = '127.0.0.1'
PORT = 4200
HEADERLEN = 10

srvr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srvr.bind((HOST, PORT))
srvr.listen()

sockets = [srvr]
clients = {}


def getMsg(skt):
    full_msg = ''
    new = True
    while True:
        msg = skt.recv(HEADERLEN)
        if new:
            msglen = int(msg)
            new = False
        if len(msg) == 0:
            break
        full_msg += msg.decode()
        if len(full_msg)-HEADERLEN == msglen:
            return full_msg[HEADERLEN:]  # returns DECODED message


def sendMsg(clnt, msg):
    msg = f'{len(msg):<{HEADERLEN}}' + msg
    msg = msg.encode()
    clnt.send(msg)  # sends ENCODED message


def broadcast(msg):
    for i in clients:
        sendMsg(i, msg)


def threader(clnt):  # target for tread to manage clients
    while True:
        try:
            msg = getMsg(clnt)
            broadcast(msg)
        except:
            broadcast(f'{clients[clnt]} left the chat')
            del clients[clnt]
            clnt.close()
            break


def receive():
    while True:
        clnt, addr = srvr.accept()
        print(f'connected to {addr}')
        sendMsg(clnt, 'name')
        name = getMsg(clnt)
        sendMsg(clnt, 'Connected..\n')
        broadcast(f'{name} joined the chat')
        clients[clnt] = name
        thread = threading.Thread(target=threader, args=(clnt,))
        thread.start()


receive()
