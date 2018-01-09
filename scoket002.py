import socket
import threading

bind_ip = "127.0.0.1"
bind_port = 5555


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print("[*]Listen on %s:%s"%(bind_ip,bind_port))

client_socket,addr = server.accept()

def hand_client():
    while True:

        request = client_socket.recv(1024).decode()
        print('[*]Received:%s'%request)
        break
def handle_send():

    while True:

        content = input("请输入回复信息：")
        client_socket.send(content.encode())
        break

print("[*]Accept connection from :%s:%s"%(addr[0],addr[1]))

client_hander = threading.Thread(target=hand_client,args=())
client_hander.start()
sender_hander = threading.Thread(target=handle_send(),args=())
sender_hander.start()

