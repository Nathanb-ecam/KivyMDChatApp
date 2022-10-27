# Transfert de données au serveur 

import json
import socket


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5566 # localhost est l'adresse du serveur local equivalent a l'ip 127.0.0.1

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

class Client_Handling:
    def __init__(self):
        pass
    
    def _connect_to_server(self):
        try:
            client.connect((HOST,PORT)) # pour connecter le client au serveur
            self.conn = ((HOST,PORT)) 
        except Exception:
            print("Deja connecté au serveur ")


    def _disconnect_from_server(self,user):
        try:
            msg_dict = {'_disconnect':{"Username":user.name}}
            print("ENCOIE DU MESSAGE DE DECONNEXION")
            data = json.dumps(msg_dict).encode("utf-8")
            client.sendall(data)
            client.close()
        except Exception as e:
            print(e)
    
    def _send(self,msg_dict):
        data = json.dumps(msg_dict).encode("utf-8")
        try:
            client.sendall(data)
        except:
            self._connect_to_server()
            client.sendall(data)


    def _receive(self):
        # pour recevoir des données
        data = client.recv(1024) # taille de reception de données 
        data = data.decode("utf-8")
        if len(data)>0:
            data = json.loads(data)
            return data
        

    def _connectedPeople(self):
        msg_dict = {'_connected':""}
        data = json.dumps(msg_dict).encode("utf-8")
        client.sendall(data)
        data = self._receive()
        return data

    def _send_allowed_request(self,msg_dict):
        msg_dict = {'_allowed':msg_dict}
        data = json.dumps(msg_dict).encode("utf-8")
        client.sendall(data)
        data = self._receive()
        return data
