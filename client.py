import socket
import threading

HOST = '127.0.0.1'
PORT = 4200
HEADERLEN = 10

name = input("Enter nickname: ")
clnt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clnt.connect((HOST, PORT))


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


def receive():
    while True:
        try:
            msg = getMsg(clnt)
            if msg == 'name':
                sendMsg(clnt, name)
            else:
                print(msg)
        except:
            print("Error")
            clnt.close()
            break


def write():
    while True:
        msg = '{}: {}'.format(name, input())
        sendMsg(clnt, msg)


recv_thread = threading.Thread(target=receive)
recv_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
