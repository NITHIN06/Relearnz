from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen 

Window.size = (870, 580)
Window.minimum_width, Window.minimum_height = Window.size

class Main(MDApp):
    pass

class WindowManager(ScreenManager):
    pass


class Welcome(Screen):
    pass

class Login(Screen):
    a = 0
    def logger(self):
        username = self.ids.user.text
        password = self.ids.password.text

        if(username == "" or username =="FIELD SHOULD NOT BE EMPTY"):
            self.ids.user.text = "FIELD SHOULD NOT BE EMPTY"
            self.a =0
            
        if(password == "" or password =="FIELD SHOULD NOT BE EMPTY"):
            self.ids.password.text = "FIELD SHOULD NOT BE EMPTY"
            self.a =0

        if(self.a==1):
            self.manager.current= "Tdashboard"
            self.manager.transition.direction = "left"
            return 
        self.a=1    


class Register(Screen):

    t=0
    dialog=None
    a=1
    def teacher(self):
        self.t=1
    def student(self):
        self.t=-1

    def registration(self):
        username = self.ids.user.text
        email = self.ids.email.text  
        password = self.ids.password.text 
	
        if(username == "" or username =="FIELD SHOULD NOT BE EMPTY"):
            self.ids.user.text = "FIELD SHOULD NOT BE EMPTY"
            self.a=0
            
        if(password == "" or password =="FIELD SHOULD NOT BE EMPTY"):
            self.ids.password.text = "FIELD SHOULD NOT BE EMPTY"
            self.a =0

        if(email == "" or email =="FIELD SHOULD NOT BE EMPTY"):
            self.ids.email.text = "FIELD SHOULD NOT BE EMPTY"              
            self.a =0

        if( self.a ==1 and self.t==0):
            self.dialog = MDDialog(title="Select a Role")
            self.dialog.open()
            return 

        if( self.a ==1 and self.t==1):
            self.manager.current= "Tdashboard"
            self.manager.transition.direction = "left"
            return 

        if( self.a ==1 and self.t==-1):
            self.manager.current= "Sdashboard"
            self.manager.transition.direction = "left"
            return 
        self.a=1



class Tdashboard(Screen):
    pass

class Sdashboard(Screen):
    pass

Main().run()






