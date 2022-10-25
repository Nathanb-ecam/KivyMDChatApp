
from kivymd.app import MDApp

from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.list import OneLineListItem
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image




"""
_____________________________________________________________________________________CLIENT SOCKET PART_____________________________________________________________________________________
"""
from Client_Handling import Client_Handling
from User import User 
import sys





running = True



"""

_____________________________________________________________________________________INTERFACE PART_____________________________________________________________________________________ 

"""
white = (1,1,1,1)
red = (1,0,0,1)
black = (0,0,0,0)
green = [0, 1, 0, 1] 
blue = [0, 0, 1, 1] 
purple = [1, 0, 1, 1] 


client = Client_Handling()




class UserApp(MDApp):
    def connect_to_server(self):
        client._connect_to_server()
        self.connected = True
    

    def disconnect_from_server(self,instance):
        client._disconnect_from_server(self.user)
        sys.exit()
    
    def send(self,instance):
        # verifier qu'on soit connecter au serveur 
        if self.connected:
            client._send({'_transfer':{"UserInformations":{'Username':self.user.name,'Message':self.message.text,'Destinator':self.destinator}}})

    def connected_people_list(self):
        if self.connected:
            data = client._connectedPeople()
            # self.connecteds.values = data.values()
            connecteds = data.values()
        return connecteds

               
    def page_manager(self,instance):
        pages = {'_login':'loginScreen','_contact':"contactScreen",'_send':'sendScreen'}
        sm.current = pages[instance.id]
    
    def contact_selector(self,instance):
        if self.connecteds.text != "Connected Peoples": # on verifie qu'il ai bien selectionner un contact valable dans le spinner
            selected_contact = self.connecteds.text
            print("SELECTED CONTACT:",selected_contact)
            self.page_manager(instance)   
            self.destinator.text = selected_contact 


    def build(self):
        #Initialisation des variables 
        self.contacts = []
        self.ids = {}
        self.connected = False
        self.connect_to_server()

        """THEMES"""
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Light" #Dark
        self.theme_cls.primary_palette = "Blue" #Orange , Red
        """"""

       
        """
                __________________________________________________________________________________________________________________________________________________________________
        """
user = UserApp()

class LoginScreen(Screen):
    def login(self,name,password):
        print(".KV file")
        """faire une form validation avec regex"""
        #stocker les users dans un json
        self.user = User(name.text,password.text)
        print("user added")
        print(self.user)
        self.registerClient_ToServer() 
        user.root.current = "contact_screen"


    def registerClient_ToServer(self):
        if user.connected:
            client._send({'_authentification':{"UserInformations":{"Username":self.user.name,"Password":self.user.password}}})
            print("Username envoyé au SERVEUR")
        else:
            print("Not connected")

    def switch_theme(self,checkbox,value):
        if value:
            user.theme_cls.theme_style ="Dark"
            user.theme_cls.primary_palette="Orange"
        else:
            user.theme_cls.theme_style ="Light"
            user.theme_cls.primary_palette="Blue"



class ContactScreen(Screen):
    def refresh_contacts(self):
        connecteds = user.connected_people_list()
        # user.root.current = "send_screen"  
        print(self.ids.container)        
      
        for i in range(len(connecteds)):
            item = OneLineListItem(text="item" + str(i))
            # ContactScreen.ids.container.add_widget(item)
            #.container.add_widget(item)
            



class SendScreen(Screen):
    pass
class MyScreenManager(ScreenManager):
    pass





user.run()