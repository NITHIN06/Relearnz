from logging import Manager
from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', 1300)
Config.set('graphics', 'height', 750)
Config.set('graphics', 'resizable', False)

import smtplib
import socket
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton, MDIconButton,MDTextButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from firebase import firebase
import threading
import webbrowser
from datetime import datetime,date
from kivy.clock import Clock



# firebase connection
firebase = firebase.FirebaseApplication(
    "https://relearnz-default-rtdb.firebaseio.com/", None)

socket.getaddrinfo('localhost',25)

#time-table
time_table=[{"name":"Artifical Intelligence","pic":"assets/AI.png","start":9,"batch":'even',"screen":"Ai"},
            {"name":"Software Engineering And ...","pic":"assets/SEPM.png","batch":'odd',"start":9,"screen":"Sepm"},
            {"name":"Computer Forensics","pic":"assets/CF.png","start":10,"batch":'even',"screen":"Cf"},
            {"name":"Digital Signal Processing","pic":"assets/DSP.png","start":10,"batch":'odd',"screen":"Dsp"},
            {"name":"Human Resource Management","pic":"assets/HRM.png","start":11,"batch":'even',"screen":"Hrm"},
            {"name":"Operations & Supply Chain ...","pic":"assets/OSM.png","start":11,"batch":'odd',"screen":"Osm"},
            {"name":"Finanical Management","pic":"assets/FMA.png","start":12,"batch":'even',"screen":"Fma"},
            {"name":"Soft Computing","pic":"assets/SC.png","start":12,"batch":'odd',"screen":"Sc"}]

def nearest_class(l):
    time_now=datetime.now().hour
    x=[i["start"] for i in l]
    c=0
    z=[]
    for i in range(len(x)):
        if (time_now<=x[i] and len(z)!=2):
            z.append(l[i])
    return z

def tt():
    global now_next
    now_next=[]
    l=[]
    for i in time_table:
        today= date.today().day
        if (today%2==0 and i["batch"]=='even'):
            #even-> batch-even
            l.append(i)
        elif (today%2!=0 and i["batch"]=='odd'):
            #odd-> batch-odd
            l.append(i)
    now_next=nearest_class(l)
    if len(now_next)==1:
        now_next.append({"name":"NONE","pic":"assets/female.png","screen":"Sdashboard"})
    elif len(now_next)==0:
        now_next.append({"name":"NONE","pic":"assets/female.png","screen":"Sdashboard"})
        now_next.append({"name":"NONE","pic":"assets/female.png","screen":"Sdashboard"})


class WindowManager(ScreenManager):
    pass

class Welcome(Screen):
    pass

class Login(Screen):
    a = 1
    dialog = None

    def login(self):
        self.load()
        threading.Thread(target=self.logger).start()

    def load(self):
        if self.ids.load.active == False:
            self.ids.load.active = True
        else:
            self.ids.load.active = False

    def account_checker(self, username, password):
        global user_id
        global user_info
        users_list1 = firebase.get("/Users/Teacher", '')
        users_list2 = firebase.get("/Users/Student", '')
        users_list2.update(users_list1)
        for i in users_list2:
            if users_list2[i]["username"] == username and users_list2[i]["password"] == password:
                user_id = i
                user_info = users_list2[i]
                return users_list2[i]["role"]

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
        threading.Thread(target=self.registration).start()

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
        global user_id
        global user_info

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

            # store the values in the database
            info = {"username": username, "email": email,
                    "password": password, "role": self.t}
            x = firebase.post("/Users/Teacher", info)
            user_id = x['name']
            user_info = info
            self.ids.btn_tch.icon = "assets/teacher.png"
            self.ids.btn_std.icon == "assets/student.png"
            self.ids.user.text = ""
            self.ids.password.text = ""
            self.ids.email.text = ""
            self.t = 0
            self.ids.load.active = False

            self.manager.current = "Tdashboard"
            self.manager.transition.direction = "left"

        if(self.a == 1 and self.t == -1):

            # store the values in the database

            courses={"AI":{"Labs":[],"Assignments":[],"Attendence":75},
                    "SEPM":{"Labs":[],"Assignments":[],"Attendence":70},
                    "CF":{"Labs":[],"Assignments":[],"Attendence":85},
                    "SC":{"Labs":[],"Assignments":[],"Attendence":74},
                    "DSP":{"Labs":[],"Assignments":[],"Attendence":95},
                    "HRM":{"Labs":[],"Assignments":[],"Attendence":55},
                    "OSM":{"Labs":[],"Assignments":[],"Attendence":45},
                    "FMA":{"Labs":[],"Assignments":[],"Attendence":78}}

            info = {"username": username, "email": email,
                    "password": password, "role": self.t,
                    "courses":courses}
            x = firebase.post("/Users/Student", info)
            user_id = x['name']
            user_info = info
            self.ids.btn_tch.icon = "assets/teacher.png"
            self.ids.btn_std.icon == "assets/student.png"
            self.ids.user.text = ""
            self.ids.password.text = ""
            self.ids.email.text = ""
            self.t = 0
            self.ids.load.active = False

            self.manager.current = "Sdashboard"
            self.manager.transition.direction = "left"

        self.ids.load.active = False
        self.a = 1

class Tdashboard(Screen):
    def __init__(self,**kwargs):
        try:
            super(Tdashboard,self).__init__(**kwargs)
            Clock.schedule_interval(self.update,0.5)
        except:
            pass  
    def update(self,*args):
        try:
            self.ids.uname.text = "Hello "+str(user_info["username"])
        except:
            pass


class Sdashboard(Screen):
    def __init__(self,**kwargs):
        try:
            super(Sdashboard,self).__init__(**kwargs)
            Clock.schedule_interval(self.update,0.5)
        except:
            pass  
    def update(self,*args):
        try:
            self.ids.uname.text = "Hello "+str(user_info["username"])
        except:
            pass

class ClockLabel(Label):
    def __init__(self,**kwargs):
        super(ClockLabel,self).__init__(**kwargs)
        Clock.schedule_interval(self.update,1)
    def update(self,*args):
        self.text= f"{datetime.now().strftime('%H:%M')}"

class NowIcon(MDIconButton):
    def __init__(self, **kwargs):
        super(NowIcon,self).__init__(**kwargs)
        Clock.schedule_interval(self.update_class_icon,5)
    def update_class_icon(self,*args):
        tt()
        self.screen=now_next[0]["screen"]
        self.icon=now_next[0]["pic"]

class NowText(MDTextButton):
    def __init__(self, **kwargs):
        super(NowText,self).__init__(**kwargs)
        Clock.schedule_interval(self.update_class_text,5)

    def update_class_text(self,*args):
        tt()
        self.screen=now_next[0]["screen"]
        self.text=now_next[0]["name"]

class NextIcon(MDIconButton):
    def __init__(self, **kwargs):
        super(NextIcon,self).__init__(**kwargs)
        Clock.schedule_interval(self.update_class_icon,5)
    def update_class_icon(self,*args):
        tt()
        self.screen=now_next[1]["screen"]
        self.icon=now_next[1]["pic"]

class NextText(MDTextButton):
    def __init__(self, **kwargs):
        super(NextText,self).__init__(**kwargs)
        Clock.schedule_interval(self.update_class_text,5)
    def update_class_text(self,*args):
        tt()
        self.screen=now_next[1]["screen"]
        self.text=now_next[1]["name"]

class TodayDate(MDLabel):
    def __init__(self, **kwargs):
        super(TodayDate,self).__init__(**kwargs)
        Clock.schedule_interval(self.update_date,5)
    def update_date(self,*args):
        self.text=str(datetime.now().day)+"-"+str(datetime.now().month)+"-"+str(datetime.now().year)

class Scourse(Screen):
    pass
class Tcourse(Screen):
    pass

class Sevent(Screen):
    pass
class Tevent(Screen):
    pass

class Schat(Screen):
    pass
class Tchat(Screen):
    pass

class Sannouncement(Screen):
    pass
class Tannouncement(Screen):
    pass

class Tfeedback(Screen):
    pass

class Sfeedback(Screen):
    def feedback_send(self):
        # server= smtplib.SMTP("smtp.gmail.com",587)
        # server.ehlo()
        # server.starttls()
        # server.login("vajrapusugnankranthiraju@gmail.com","yqqladmhfdgmuoes")
        # From="vajrapusugnankranthiraju@gmail.com"
        # To="akhilsaibande13@gmail.com"
        txt=self.ids.feedback_txt.text

        # body="""Subject: Feedback from %s\n
        #         %s"""%(user_info['username'],txt)
        # self.server.sendmail(From,[To],body)
        x=firebase.get('Users/Student','')
        for i in x:
            if len(txt)<10:
                firebase.post('Users/Student/'+i+'/courses/AI/Labs',{'question':txt,'sender':user_info['username'],'time':f"{datetime.now().strftime('%H:%M')}"})
            else:
                firebase.post('Users/Student/'+i+'/courses/AI/Assignments',{'question':txt,'sender':user_info['username'],'time':f"{datetime.now().strftime('%H:%M')}"})

        self.ids.feedback_txt.text = ""
        return

class Sprofile(Screen):
    def __init__(self, **kwargs):
        try:
            super(Sprofile,self).__init__(**kwargs)
            Clock.schedule_interval(self.update_profile,0.5)
        except:
            pass
    def update_profile(self,*args):
        try:
            self.ids.pro_name.text=user_info["username"]
            self.ids.pro_email.text=user_info["email"]
        except:
            pass

class Tprofile(Screen):
    def __init__(self, **kwargs):
        try:
            super(Tprofile,self).__init__(**kwargs)
            Clock.schedule_interval(self.update_profile,0.5)
        except:
            pass
    def update_profile(self,*args):
        try:
            self.ids.pro_name.text=user_info["username"]
            self.ids.pro_email.text=user_info["email"]
        except:
            pass    

class Ai(Screen):
    def joinclass(self):
        webbrowser.open('https://meet.google.com/jpq-webf-iwy?pli=1', new = 1)
class Cf(Screen):
    def joinclass(self):
        webbrowser.open('https://meet.google.com/jpq-webf-iwy?pli=1', new = 1)
class Dsp(Screen):
    def joinclass(self):
        webbrowser.open('https://meet.google.com/jpq-webf-iwy?pli=1', new = 1)
class Hrm(Screen):
    def joinclass(self):
        webbrowser.open('https://meet.google.com/jpq-webf-iwy?pli=1', new = 1)
class Sc(Screen):
    def joinclass(self):
        webbrowser.open('https://meet.google.com/jpq-webf-iwy?pli=1', new = 1)
class Sepm(Screen):
    def joinclass(self):
        webbrowser.open('https://meet.google.com/jpq-webf-iwy?pli=1', new = 1)
class Fma(Screen):
    def joinclass(self):
        webbrowser.open('https://meet.google.com/jpq-webf-iwy?pli=1', new = 1)
class Osm(Screen):
    def joinclass(self):
        webbrowser.open('https://meet.google.com/jpq-webf-iwy?pli=1', new = 1)

class Main(MDApp):
    pass


Main().run()


