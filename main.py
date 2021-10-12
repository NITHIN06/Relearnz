from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
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
    dialog=None
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

            self.ids.load.active=True
            if(1): # search for inputs in teacher database 
                self.manager.current= "Tdashboard"
                self.manager.transition.direction = "left"

            elif(1): # search for inputs in student database 
                self.manager.current= "Sdashboard"
                self.manager.transition.direction = "left"
            else:
                self.dialog = MDDialog(title="Invalid Login", text="Enter correct credentials or signup if you don't have an account", radius=[20, 7, 20, 7])
                self.dialog.open()
            self.ids.load.active=False
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
            self.dialog = MDDialog(title="Select a Role", text="Please select either Teacher or Student role", radius=[20, 7, 20, 7])
            self.dialog.open()
            return 

        if( self.a ==1 and self.t==1):
            self.ids.load.active=True

            # store the values in the database

            self.manager.current= "Tdashboard"
            self.manager.transition.direction = "left"
            self.ids.load.active=False
            return 

        if( self.a ==1 and self.t==-1):
            self.ids.load.active=True

            # store the values in the database   
         
            self.manager.current= "Sdashboard"
            self.manager.transition.direction = "left"
            self.ids.load.active=False
            return 
        self.a=1



class Tdashboard(Screen):
    pass

class Sdashboard(Screen):
    pass

Main().run()






