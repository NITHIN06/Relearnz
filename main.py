from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', 870)
Config.set('graphics', 'height', 580)
Config.set('graphics', 'resizable', False)


from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivy.uix.screenmanager import ScreenManager, Screen
from firebase import firebase
import threading

# firebase connection
firebase = firebase.FirebaseApplication(
    "https://relearnz-default-rtdb.firebaseio.com/", None)


class Main(MDApp):
    pass


class WindowManager(ScreenManager):
    pass


class Welcome(Screen):
    pass


class Login(Screen):

    a = 1
    dialog = None

    def login(self):
        self.load()
        threading.Thread(target = self.logger).start()


    def load(self):
        if self.ids.load.active == False:
            self.ids.load.active = True
        else:
            self.ids.load.active = False

    def account_checker(self, username, password):
        users_list = firebase.get("/Users", '')
        for i in users_list:
            if users_list[i]["username"] == username and users_list[i]["password"] == password:
                return users_list[i]["role"]

    def logger(self):
        username = self.ids.user.text
        password = self.ids.password.text

        if(username == "" or username == "FIELD SHOULD NOT BE EMPTY"):
            self.ids.user.text = "FIELD SHOULD NOT BE EMPTY"
            self.a = 0


        if(password == "" or password == "FIELD SHOULD NOT BE EMPTY"):
            self.ids.password.text = "FIELD SHOULD NOT BE EMPTY"
            self.a = 0


        if(self.a == 1):

            # search for inputs in teacher database
            if(self.account_checker(username, password) == 1):
                self.manager.current = "Tdashboard"
                self.manager.transition.direction = "left"

            # search for inputs in student database
            elif(self.account_checker(username, password) == -1):
                self.manager.current = "Sdashboard"
                self.manager.transition.direction = "left"

            else:
                self.dialog = MDDialog(
                    title="Invalid Login", text="Enter correct credentials or signup if you don't have an account", radius=[20, 7, 20, 7])
                self.dialog.open()

            self.ids.user.text = ""
            self.ids.password.text = ""

        self.load()    
        self.a = 1


class Register(Screen):

    t = 0
    dialog = None
    a = 1

    def load(self):
        if self.ids.load.active == False:
            self.ids.load.active = True
        else:
            self.ids.load.active = False

    def register(self):
        self.load()
        threading.Thread(target = self.registration).start()

    def teacher(self):
        if self.ids.btn_tch.icon == "assets/teacher.png":
            self.ids.btn_tch.icon = "assets/check.png"
            self.ids.btn_std.icon = "assets/student.png"
        else:
            self.ids.btn_tch.icon = "assets/teacher.png"
        self.t = 1

    def student(self):
        if self.ids.btn_std.icon == "assets/student.png":
            self.ids.btn_std.icon = "assets/check.png"
            self.ids.btn_tch.icon = "assets/teacher.png"
        else:
            self.ids.btn_std.icon = "assets/student.png"
        self.t = -1

    def registration(self):
        username = self.ids.user.text
        email = self.ids.email.text
        password = self.ids.password.text

        if(username == "" or username == "FIELD SHOULD NOT BE EMPTY"):
            self.ids.user.text = "FIELD SHOULD NOT BE EMPTY"
            self.a = 0

        if(password == "" or password == "FIELD SHOULD NOT BE EMPTY"):
            self.ids.password.text = "FIELD SHOULD NOT BE EMPTY"
            self.a = 0

        if(email == "" or email == "FIELD SHOULD NOT BE EMPTY"):
            self.ids.email.text = "FIELD SHOULD NOT BE EMPTY"
            self.a = 0

        if(self.ids.btn_std.icon == "assets/student.png" and self.ids.btn_tch.icon == "assets/teacher.png"):
            self.dialog = MDDialog(
                title="Select a Role", text="Please select either Teacher or Student role", radius=[20, 7, 20, 7])
            self.dialog.open()
            return

        if(self.a == 1 and self.t == 1):
            self.ids.load.active = True

            # store the values in the database
            info = {"username": username, "email": email,
                    "password": password, "role": self.t}
            firebase.post("/Users", info)

            self.ids.btn_tch.icon = "assets/teacher.png"
            self.ids.btn_std.icon == "assets/student.png"
            self.ids.user.text = ""
            self.ids.password.text = ""
            self.ids.email.text = ""
            self.t = 0

            self.manager.current = "Tdashboard"
            self.manager.transition.direction = "left"

        if(self.a == 1 and self.t == -1):
            self.ids.load.active = True

            # store the values in the database
            info = {"username": username, "email": email,
                    "password": password, "role": self.t}
            firebase.post("/Users", info)
            self.ids.btn_tch.icon = "assets/teacher.png"
            self.ids.btn_std.icon == "assets/student.png"
            self.ids.user.text = ""
            self.ids.password.text = ""
            self.ids.email.text = ""
            self.t = 0

            self.manager.current = "Sdashboard"
            self.manager.transition.direction = "left"

        self.load()
        self.a = 1


class Tdashboard(Screen):
    pass


class Sdashboard(Screen):
    pass


Main().run()
