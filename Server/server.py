from datetime import datetime
import socket
import threading
import json

import time
from Server_Options import Server_Options
from User import User

SERVER = socket.gethostbyname(socket.gethostname())
print("SERVER :",SERVER)
PORT = 5566 # le serveur n'a pas besoin d'adresse car il ne fait qu'ecouter
print("PORT :",PORT)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((SERVER, PORT))
print("Le serveur est démarré ... ",sep='\n')

""" We retrieve allowed people to access the app from a txt file

"""
def get_allowed_people():
    allowed_people = read_users_from_file()
    return allowed_people


def read_users_from_file():
    users = []
    with open("./Server/users.txt","r") as f:
        print("#######################")
        print("All allowed people \n")
        for line in f.readlines():
            print(line.rstrip())
            users.append(json.loads(line.rstrip()))
        print("#######################")
    return users


def write_users_to_file():
    with open("./Server/users.txt","w") as f:
        for client in _connected_people:
            f.write(json.dumps(_connected_people[client])+"\n")



_connected_people = dict()
_allowed_people = get_allowed_people()



Options = Server_Options()

# pour gerer plusieur connexion de client simultanément 
class AppServer(threading.Thread): 
    def __init__(self,conn,addr,client = {}):
        threading.Thread.__init__(self)
        self.conn = conn 
        self.client = client
        self.host = addr[0]
        self.port = server.getsockname()[1]

    def _authentification(self,auth):
        username,password,image = auth
        user = User(username,password,image)
        # l = []
        # for username in _connected_people:
        #     l.append(_connected_people[username]["Username"])

        number_of_clients = len(_connected_people)
        # if username not in l:
        _connected_people["Client"+str(number_of_clients)] = {"Username":user.name,"Password":user.password,"Image":user.image}
            
    def _disconnect_from_server(self,Username):
        print(f"{Username} vient de se déconnecter")
        #eviter la boucle
        for client in _connected_people:
            if _connected_people[client]['Username'] == Username:
                _connected_people.pop(client)
   

    def _connected_people(self):
        answer = json.dumps(_connected_people).encode("utf-8")
        self.conn.send(answer)


    def _transfer_message(self,sender,message,destinator):
        print("Expeditor :",sender)
        print("Message :",message)
        print("Destinator :",destinator)

    def _is_allowed(self,name,password):
        for client in _allowed_people:
            if client["Username"]==name and client["Password"] ==password:
                msg_dict = {"_allowed":{"status":"Acces Authorized"}}
                break
        try:
            answer = json.dumps(msg_dict).encode("utf-8") 
        except:
            answer = json.dumps({"_allowed":{"status":"Acces Refused"}}).encode("utf-8")
        finally:
            self.conn.send(answer)

    def _receive(self):
        handlers = {"_authentification":self._authentification,"_connected":self._connected_people,"_disconnect":self._disconnect_from_server,'_receive':self._receive,"_transfer":self._transfer_message,"_allowed":self._is_allowed}
        try:
            data = self.conn.recv(1024) # taille de reception de données 
            data = data.decode("utf-8")
            data = json.loads(data)
            print("Received DATA :\n",data)
            print("________________________________")
            print("Connected people :\n",_connected_people)
            print("________________________________")

            for key in data:
                if key in handlers:
                    print("Action ... \t",key[1:])
                    if key==Options.registered:
                        handlers[key]((data[Options.registered]["UserInformations"]["Username"],data[Options.registered]["UserInformations"]["Password"],data[Options.registered]["UserInformations"]["Image"]))
                    elif key==Options.disconnected:
                        handlers[key](data[Options.disconnected]["Username"])
                    elif key==Options.transfer:
                        handlers[key](data[Options.transfer]["UserInformations"]["Username"],data[Options.transfer]["UserInformations"]["Message"],data[Options.transfer]["UserInformations"]['Destinator'])
                    elif key==Options.allowed:
                        handlers[key](data[Options.allowed]["Username"],data[Options.allowed]["Password"]) 
                    elif key==Options.connecteds:
                        handlers[key]()
                    else:
                        handlers[key]()
            print("Attend des nouvelles requetes ...")
            self._receive()
        except Exception as e:
            print(e)
        
    def run(self):
        self._receive()



            

# boucle infinie pour que le serveur ecoute tant qu'une machine est connectée
while True:
    server.listen(5) # le parametre est le nombre de connexion qui peuvent échouer avant de refuser d'autres connexions
    conn, addr = server.accept() # on stocke les info de la machine qui est actuellement connectée au serveur adress contient ip et le port 
    print(f"Un client de la connexion {addr[0]} vient de se connecter à {datetime.now()} sur le port {server.getsockname()[1]}")
    
    
    # conn.send(answer)

    my_thread = AppServer(conn,addr)
    my_thread.start() # appelle la méthode run de la classe ClientsHandling

conn.close()
server.close()