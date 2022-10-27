
from kivymd.app import MDApp

from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.list import OneLineListItem,ThreeLineListItem,OneLineAvatarListItem,ImageLeftWidget,IconLeftWidget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, NumericProperty,StringProperty
from kivymd.icon_definitions import md_icons


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
    
    def disconnect_from_server(self):
        client._disconnect_from_server(self.user)
        

    def send(self,expeditor,message,destinator):
        # verifier qu'on soit connecter au serveur 
        if self.connected:
            client._send({'_transfer':{"UserInformations":{'Username':expeditor,'Message':message,'Destinator':destinator}}})

    def is_allowed(self,name,password): # if not in the file, not allowed to log in 
        if self.connected:
            allowed = client._send_allowed_request({"Username":name,"Password":password})
        return allowed

    def connected_people_list(self):
        if self.connected:
            data = client._connectedPeople()
            # self.connecteds.values = data.values()
            connecteds = data.values()
        return connecteds

    def build(self):
        #Initialisation des variables 
        self.user = ""
        self.allUsers = [] # object of type User list
        self.contacts = []
        self.logged = False # boolean to check if user in database
        self.ids = {}
        self.connected = False
        self.connect_to_server()

        """THEMES"""
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Light" #Dark
        self.theme_cls.primary_palette = "Blue" #Orange , Red
        """"""

userApp = UserApp()

class LoginScreen(Screen):
    def login(self,name,password):
        """faire une form validation avec regex"""
        allowed = userApp.is_allowed(name.text,password.text)
        print(allowed)
        if allowed["_allowed"]["status"]=="Acces Authorized":
            userApp.logged=True
            

        if userApp.logged:
            #stocker les users dans un json
            userApp.user = User(name.text,password.text,"../Assets/v.jpg")
            print("user added")
            print(userApp.user)
            self.registerClient_ToServer() 
            userApp.root.current = "contact_screen"


    def registerClient_ToServer(self):
        if userApp.connected:
            client._send({'_authentification':{"UserInformations":{"Username":userApp.user.name,"Password":userApp.user.password,"Image":userApp.user.image}}})
            print("Username envoyé au SERVEUR")
        else:
            print("Not connected")

    def switch_theme(self,checkbox,value):
        if value:
            userApp.theme_cls.theme_style ="Dark"
            userApp.theme_cls.primary_palette="Orange"
        else:
            userApp.theme_cls.theme_style ="Light"
            userApp.theme_cls.primary_palette="Blue"



class ContactScreen(Screen):
    def refresh_contacts(self):
        connecteds = userApp.connected_people_list()
        self.ids.container.clear_widgets()
        contact_names=[]
        for contact in connecteds:
            if contact["Username"] not in contact_names and contact["Username"]!=userApp.user.name:
                contact_names.append(contact["Username"])



        for username in contact_names:
            item = OneLineListItem(text=username)
            item.id =username
            item.bind(on_press=self.go_to_contact)
            self.ids.container.add_widget(item)

    def go_to_contact(self,instance):
        self.manager.get_screen("send_screen").ids.destinator.text = instance.text
        if instance.text in userApp.allUsers:
            self.manager.get_screen("send_screen").ids.destinator_image.source = userApp.user.image
        
        self.load_contact_page(instance.text)
        userApp.root.current = "send_screen"

    def load_contact_page(self,contact):
        pass

    def quit(self):
        userApp.disconnect_from_server()
        sys.exit()
            



class SendScreen(Screen):
    def send_message(self):
        message = self.ids.message.text
        userApp.send(userApp.user.name,message,self.ids.destinator.text)
        

    
class MyScreenManager(ScreenManager):
    pass





userApp.run()