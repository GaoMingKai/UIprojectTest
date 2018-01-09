import socket
import os,threading
import json

bind_ip = "127.0.0.1"
bind_point = 8000
timeout = 30

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((bind_ip,bind_point))
server.listen(5)
while True:
    client_socket,addr = server.accept()
    try:
        client_socket.settimeout(30)
        request = client_socket.recv(1024).decode()
        try:
            request = json.loads(request)
        except:
            pass
        if isinstance(request,dict):
            if request.get("name","") == "kirry" and request.get("passwd","") == "123456":
                client_socket.send("master please order!".encode())
                while True:
                    client_socket,addr = server.accept()
                    data = client_socket.recv(1024).decode()
                    data = eval(data)
                    client_socket.send(data.encode())
        else:
            client_socket.send("welcome our computer!")
    except:
        print("等待30s后没有链接接入！")
    client_socket.close()
