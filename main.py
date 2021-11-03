from logging import Manager
from os import close
from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', 1300)
Config.set('graphics', 'height', 750)
Config.set('graphics', 'resizable', False)

import smtplib
import pandas as pd
import socket
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton, MDIconButton,MDTextButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.snackbar import Snackbar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from firebase import firebase
import threading
import webbrowser
from datetime import datetime,date
import time
from kivymd.uix.textfield import MDTextField
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivymd.uix.list import OneLineAvatarIconListItem,MDList,TwoLineAvatarListItem,ImageLeftWidget
from kivy.properties import StringProperty
import re

# firebase connection
firebase = firebase.FirebaseApplication(
    "https://relearnz-default-rtdb.firebaseio.com/", None)

socket.getaddrinfo('localhost',25)

#time-table
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/1UVyCrSjX4pX2La2JW9IOtmpkkfaNaW_sN4-nAPpELgU/export?format=csv")
times=list(df['Time'])


t = time.localtime()
current_time = datetime.strptime(str(t.tm_hour)+":"+str(t.tm_min), '%H:%M')
time_table1={
    "AI":{'name':"Artifical Intelligence","pic":"assets/AI.png","screen":"Ai"},
    "SEPM":{"name":"Software Engineering And ...","pic":"assets/SEPM.png","screen":"Sepm"},
    "CF":{"name":"Computer Forensics","pic":"assets/CF.png","screen":"Cf"},
    "DSP":{"name":"Digital Signal Processing","pic":"assets/DSP.png","screen":"Dsp"},
    "HRM":{"name":"Human Resource Management","pic":"assets/HRM.png","screen":"Hrm"},
    "OSM":{"name":"Operations & Supply Chain ...","pic":"assets/OSM.png","screen":"Osm"},
    "FMA":{"name":"Finanical Management","pic":"assets/FMA.png","screen":"Fma"},
    "SC":{"name":"Soft Computing","pic":"assets/SC.png","screen":"Sc"},
    "NONE":{"name":"NONE","pic":"assets/female.png","screen":"Sdashboard"}
}

def tt():
    global now_next
    t = time.localtime()
    current_time = datetime.strptime(str(t.tm_hour)+":"+str(t.tm_min), '%H:%M')
    now_next=[]
    for i in range(len(times)):
        h=[datetime.strptime(j, '%I:%M %p') for j in times[i].split(" - ")]
        if(i!=len(times)-1):
            hn=[datetime.strptime(j, '%I:%M %p') for j in times[i+1].split(" - ")]
        # try:
        if(h[0]<=current_time and h[1]>=current_time):
            no=list(df.index[df['Time']==times[i]])
            if(no[0]<len(times)-1):
                now_next.append(time_table1[df.iloc[no[0]].loc[time.ctime().split()[0]]])
                now_next.append(time_table1[df.iloc[no[0]+1].loc[time.ctime().split()[0]]])
            elif no[0]==len(times)-1:
                now_next.append(time_table1[df.iloc[no[0]].loc[time.ctime().split()[0]]])
                now_next.append(time_table1["NONE"])
        elif h[1]<current_time and hn[0]>current_time:
            no=list(df.index[df['Time']==times[i+1]])
            if(no[0]<len(times)-1):
                now_next.append(time_table1[df.iloc[no[0]].loc[time.ctime().split()[0]]])
                now_next.append(time_table1[df.iloc[no[0]+1].loc[time.ctime().split()[0]]])
            elif no[0]==len(times)-1:
                now_next.append(time_table1[df.iloc[no[0]].loc[time.ctime().split()[0]]])
                now_next.append(time_table1["NONE"])
        # except Exception as e:
        #     print("hello")
    if len(now_next)==0:
        now_next.append(time_table1["NONE"])
        now_next.append(time_table1["NONE"])

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
        z = 0
        regex = r'[\s]*'

        if(re.fullmatch(regex, username)):
            self.ids.user.text = ""
            self.a = 0
            z = 1
            self.dialog = MDDialog(
                title="Invalid Username", text="Username should not be empty", radius=[20, 7, 20, 7])
            self.dialog.open()

        if(re.fullmatch(regex, password)and z == 0):
            self.ids.password.text = ""
            self.a = 0
            self.dialog = MDDialog(
                title="Invalid Password", text="Password should not be empty", radius=[20, 7, 20, 7])
            self.dialog.open()

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

class Item(OneLineAvatarIconListItem):
    divider = None
    source = StringProperty()

class Register(Screen):

    t = 0
    dialog = None
    d = None
    course = ""
    c_id=""
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

    def ai(self, inst):
        self.course = "Artificial Intelligence"
        self.c_id = "AI"

        self.d = MDDialog(
            title="Confirm ?",
            text="Are you sure you want to select Artificial intelligence",
            radius=[20, 7, 20, 7],
            buttons=[
                MDFlatButton(text="NO", on_press=self.no),
                MDFlatButton(text="YES",on_press=self.yes),
            ],
        )
        self.d.open()

    def sepm(self, inst):
        self.course = "Software Engineering and Project Management"
        self.c_id = "SEPM"

        self.d = MDDialog(
            title="Confirm ?",
            text="Are you sure you want to select Software Engineering and Project Management",
            radius=[20, 7, 20, 7],
            buttons=[
                MDFlatButton(text="NO", on_press=self.no),
                MDFlatButton(text="YES",on_press=self.yes),
            ],
        )
        self.d.open()

    def dsp(self, inst):
        self.course = "Digital Signal Processing"
        self.c_id = "DSP"

        self.d = MDDialog(
            title="Confirm ?",
            text="Are you sure you want to select Digital Signal Processing",
            radius=[20, 7, 20, 7],
            buttons=[
                MDFlatButton(text="NO", on_press=self.no),
                MDFlatButton(text="YES",on_press=self.yes),
            ],
        )
        self.d.open()

    def sc(self, inst):
        self.course = "Soft Computing"
        self.c_id = "SC"

        self.d = MDDialog(
            title="Confirm ?",
            text="Are you sure you want to select Soft Computing",
            radius=[20, 7, 20, 7],
            buttons=[
                MDFlatButton(text="NO", on_press=self.no),
                MDFlatButton(text="YES",on_press=self.yes),
            ],
        )
        self.d.open()

    def hrm(self, inst):
        self.course = "Human Resource Management"
        self.c_id = "HRM"
        self.d = MDDialog(
            title="Confirm ?",
            text="Are you sure you want to select Human Resource Management",
            radius=[20, 7, 20, 7],
            buttons=[
                MDFlatButton(text="NO", on_press=self.no),
                MDFlatButton(text="YES",on_press=self.yes),
            ],
        )
        self.d.open()

    def cf(self, inst):
        self.course = "Computer Forensics"
        self.c_id = "CF"

        self.d = MDDialog(
            title="Confirm ?",
            text="Are you sure you want to select Computer Forensics",
            radius=[20, 7, 20, 7],
            buttons=[
                MDFlatButton(text="NO", on_press=self.no),
                MDFlatButton(text="YES",on_press=self.yes),
            ],
        )
        self.d.open()

    def fma(self, inst):
        self.course = "Financial Management & Accounting"
        self.c_id = "FMA"

        self.d = MDDialog(
            title="Confirm ?",
            text="Are you sure you want to select Financial Management & Accounting",
            radius=[20, 7, 20, 7],
            buttons=[
                MDFlatButton(text="NO", on_press=self.no),
                MDFlatButton(text="YES",on_press=self.yes),
            ],
        )
        self.d.open()

    def osm(self, inst):
        self.course = "Operations & Supply Chain Management"
        self.c_id = "OSM"

        self.d = MDDialog(
            title="Confirm ?",
            text="Are you sure you want to select Operations & Supply Chain Management",
            radius=[20, 7, 20, 7],
            buttons=[
                MDFlatButton(text="NO", on_press=self.no),
                MDFlatButton(text="YES",on_press=self.yes),
            ],
        )
        self.d.open()

    def yes(self, inst):
        global user_id
        global user_info

        info = {"username": self.ids.user.text, "email": self.ids.email.text,
        "password": self.ids.password.text, "role": self.t,
        "course":{"name":self.course,"cid":self.c_id}}
        x = firebase.post("/Users/Teacher", info)
        user_id = x['name']
        user_info = info

        self.d.dismiss()
        self.dialog.dismiss()
        self.ids.btn_tch.icon = "assets/teacher.png"
        self.ids.btn_std.icon == "assets/student.png"
        self.ids.user.text = ""
        self.ids.password.text = ""
        self.ids.email.text = ""
        self.t = 0
        self.ids.load.active = False
        self.manager.current = "Tdashboard"
        self.manager.transition.direction = "left"

    def no(self, inst):
        self.d.dismiss()

    def registration(self):
        username = self.ids.user.text
        email = self.ids.email.text
        password = self.ids.password.text
        regexe = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        regex = r'[\s]*'
        alert, alert1, alert2, alert3 = 0, 0, 0, 0
        global user_id
        global user_info

        if(username == "" or username == "FIELD SHOULD NOT BE EMPTY"):
            self.ids.user.text = "FIELD SHOULD NOT BE EMPTY"
        if(re.fullmatch(regex, username)):
            self.ids.user.text = ""
            self.a = 0
            alert = 1
            alert1 = 1
            alert2 = 1
            alert3 = 1
            self.dialog = MDDialog(
                title="Invalid Field", text="Username should not be empty", radius=[20, 7, 20, 7])
            self.dialog.open()

        if(re.fullmatch(regex, email) and alert3 == 0):
            self.ids.email.text = ""
            self.a = 0
            alert1 = 1
            alert = 1
            alert2 = 1
            self.dialog = MDDialog(
                title="Invalid Field", text="Email should not be empty", radius=[20, 7, 20, 7])
            self.dialog.open()

        if(re.fullmatch(regex, password) and alert2 == 0):
            self.ids.password.text = ""
            self.a = 0
            alert = 1
            alert1 = 1
            self.dialog = MDDialog(
                title="Invalid Field", text="Password should not be empty", radius=[20, 7, 20, 7])
            self.dialog.open()

        if(not(re.fullmatch(regexe, email)) and alert1 == 0):
            self.dialog = MDDialog(
                title="Invalid Email", text="Please enter a valid email", radius=[20, 7, 20, 7])
            self.dialog.open()
            self.a = 0
            alert = 1

        if(self.ids.btn_std.icon == "assets/student.png" and self.ids.btn_tch.icon == "assets/teacher.png" and alert == 0):
            self.dialog = MDDialog(
                title="Select a Role", text="Please select either Teacher or Student role", radius=[20, 7, 20, 7])
            self.dialog.open()
            self.a = 0

        if(self.a == 1 and self.t == 1):

            self.dialog = MDDialog(
                title="Select a Course",
                type="simple",
                items=[
                    Item(text="Artificial Intelligence", source="assets\AI.png", on_press=self.ai),
                    Item(text="Software Engineering and Project Management", source="assets\SEPM.png", on_press=self.sepm),
                    Item(text="Digital Signal Processing", source="assets\DSP.png", on_press=self.dsp),
                    Item(text="Computer Forensics", source="assets\CF.png", on_press=self.cf),
                    Item(text="Soft Computing", source="assets\SC.png", on_press=self.sc),
                    Item(text="Human Resource Management", source="assets\HRM.png", on_press=self.hrm),
                    Item(text="Financial Management & Accounting", source="assets\FMA.png", on_press=self.fma),
                    Item(text="Operations & Supply Chain Management", source="assets\OSM.png", on_press=self.osm),
                ],
            )
            self.dialog.open()


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
                    "password": password, "role": self.t}
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

    dialog = None

    def __init__(self, **kw):
        super(Tcourse, self).__init__(**kw)
        # Clock.schedule_interval(self.on_enter,5)

    def joinclass(self):
        webbrowser.open('https://meet.google.com/jpq-webf-iwy?pli=1', new = 1)

    def addlab(self):
        self.dialog = MDDialog(
            title="ADD LAB",
            type="custom",
            content_cls=Lab(),
            buttons=[
                MDFlatButton(text="CANCEL", on_press = self.cancel),
                MDFlatButton(text="OK", on_press = self.lab_ok),
            ],
        )
        self.dialog.open()

    def addassignment(self):
        self.dialog = MDDialog(
            title="ADD ASSIGNMENT",
            type="custom",
            content_cls=Assignment(),
            buttons=[
                MDFlatButton(text="CANCEL", on_press = self.cancel),
                MDFlatButton(text="OK", on_press = self.assign_ok),
            ],
        )
        self.dialog.open()

    def addnotes(self):
        pass

    def lab_ok(self, inst):
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                print(obj.text)
        self.dialog.dismiss()

    def assign_ok(self, inst):
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                print(obj.text)
        self.dialog.dismiss()

    def cancel(self, inst):
        self.dialog.dismiss()

    def on_enter(self, *args):
        self.ids.tname.text = 'Dr. ' + user_info["username"]
        self.ids.tmail.text = user_info["email"]
        # add_widgets() for lab_card 

        # add_widgets() for assignment_card 


class Lab(MDBoxLayout):
    pass

class Assignment(MDBoxLayout):
    pass

class Notes(MDBoxLayout):
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
    def __init__(self, **kw):
        super(Sannouncement,self).__init__(**kw)
        # Clock.schedule_interval(self.on_enter,5)
    def on_enter(self,*args):
        self.ids.v_list.clear_widgets()
        x= firebase.get("Announcements/",'')
        for i in reversed(x):
            card = MDCard(orientation='vertical',pos_hint={'center_x':.5 , 'center_y':.7},size_hint=(None, None),size=(880,100),border_radius=10,radius=[10],md_bg_color=[184/255,255/255,203/255,1],padding=10,elevation=0)
            icon = MDIconButton(icon='assets/'+x[i]["course"]+'.png',user_font_size=(36),pos_hint={'center_x':.5 , 'center_y':.5})
            space = MDLabel(size_hint_x=0.05)
            card_nt = MDBoxLayout(orientation='horizontal',pos_hint={'center_x':0.5 , 'center_y': 1},size_hint_y=0.001,spacing=50)
            card_name = MDLabel(text='Dr. '+x[i]["sender"]+'@'+x[i]["course"],font_style = "H6",size_hint_y=0.001)
            card_time = MDLabel(text=x[i]["time"],size_hint_y=0.001,size_hint_x = 0.7, bold=True, pos_hint={'center_x':0.8 , 'center_y':0.1})
            card_empty = MDLabel()
            card_nt.add_widget(card_name)
            card_nt.add_widget(card_empty)
            card_nt.add_widget(card_time)
            card_message = MDLabel(text=x[i]["message"],font_size=(20),size_hint_y=0.01)
            card_inner = MDBoxLayout(orientation='vertical')
            card_inner.add_widget(card_nt)
            card_inner.add_widget(card_message)
            a= MDBoxLayout(orientation='horizontal')
            a.add_widget(icon)
            a.add_widget(space)
            a.add_widget(card_inner)
            card.add_widget(a)
            self.ids.v_list.add_widget(card)

class Tannouncement(Screen):
    def announcement_send(self):
        txt=self.ids.Announcemnet_txt.text
        firebase.post("Announcements",{"message":txt,"sender":user_info["username"],"time":str(datetime.now().day)+"-"+str(datetime.now().month)+"-"+str(datetime.now().year)+"  "+str(datetime.now().hour)+"-"+str(datetime.now().minute)+"-"+str(datetime.now().second),"course":firebase.get("/Users/Teacher/"+user_id+"/", 'course/cid')})
        Snackbar(
            text="Successfully posted Announcement -_- ",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=0.5,
            pos_hint={'center_x': 0.5, 'center_y': 0.1}
        ).open()
        self.ids.Announcemnet_txt.text= ''

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
            self.ids.pro_course.text=user_info["course"]["name"]
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
