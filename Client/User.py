
# regler le probleme d'Id : gérer depuis le serveur 
class User:
    UserId= 0
    def __init__(self,Name,Password,image):
        self.name = Name
        self.password = Password
        self.image = image
        User.UserId+= 1

    def create_user_in_db(self):
        pass

    def __str__(self):
        return str(f"User : {self.name} \nPassword :{self.password} \nId {User.UserId}")
