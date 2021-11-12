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
import os
import getpass
from kivymd.uix.filemanager import MDFileManager
import pyrebase
# Authentication
from firebase_admin import auth
import firebase_admin
from firebase_admin import credentials



# firebase connection
firebase = firebase.FirebaseApplication(
    "https://relearnz-default-rtdb.firebaseio.com/", None)

config = {
    "apiKey": "AIzaSyCXGdOAi-Hj3zdUrxg4p6h0qsON3fldwts",
    "authDomain": "relearnz.firebaseapp.com",
    "databaseURL": "https://relearnz-default-rtdb.firebaseio.com",
    "projectId": "relearnz",
    "storageBucket": "relearnz.appspot.com",
    "messagingSenderId": "236774918194",
    "appId": "1:236774918194:web:dee36460c9caa85fd8542b"
    }

pyrebase = pyrebase.initialize_app(config)

auth1 = pyrebase.auth()

cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred)

storage = pyrebase.storage()

database = pyrebase.database()

socket.getaddrinfo('localhost',25)

#time-table
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/1UVyCrSjX4pX2La2JW9IOtmpkkfaNaW_sN4-nAPpELgU/export?format=csv")
times=list(df['Time'])

current_user = getpass.getuser()

t = time.localtime()
current_time = datetime.strptime(str(t.tm_hour)+":"+str(t.tm_min), '%H:%M')
time_table1={
    "AI":{'name':"Artifical Intelligence","pic":"assets/AI.png","cid":"AI", "screen" : "Scourse1"},
    "SEPM":{"name":"Software Engineering And ...","pic":"assets/SEPM.png","cid":"SEPM", "screen" : "Scourse1"},
    "CF":{"name":"Computer Forensics","pic":"assets/CF.png","cid":"CF", "screen" : "Scourse1"},
    "DSP":{"name":"Digital Signal Processing","pic":"assets/DSP.png","cid":"DSP", "screen" : "Scourse1"},
    "HRM":{"name":"Human Resource Management","pic":"assets/HRM.png","cid":"HRM", "screen" : "Scourse1"},
    "OSM":{"name":"Operations & Supply Chain ...","pic":"assets/OSM.png","cid":"OSM", "screen" : "Scourse1"},
    "FMA":{"name":"Finanical Management","pic":"assets/FMA.png","cid":"FMA", "screen" : "Scourse1"},
    "SC":{"name":"Soft Computing","pic":"assets/SC.png","cid":"SC", "screen" : "Scourse1"},
    "NONE":{"name":"NONE","pic":"assets/female.png","cid":"NONE", "screen" : "Sdashboard"}
}

course1 = ""
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
        global user_info
        global user_id
        email = self.ids.user.text
        password = self.ids.password.text
        z = 0
        regex = r'[\s]*'

        if(re.fullmatch(regex, email)):
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
            try:
                login = auth1.sign_in_with_email_and_password(email, password)
                user = auth.get_user_by_email(email)
                values=[]
                if user.email_verified == True:
                    print('Successfully fetched user data: {0}'.format(user.uid))
                    values = database.child("Users").child("Student").child(user.uid).get()
                    if values.val() is None:
                        values = database.child("Users").child("Teacher").child(user.uid).get()
                    print(values.val())
                    # search for inputs in teacher database
                    if(values.val()["role"] == 1):
                        self.manager.current = "Tdashboard"
                        self.manager.transition.direction = "left"

                    # search for inputs in student database
                    elif(values.val()["role"] == -1):
                        self.manager.current = "Sdashboard"
                        self.manager.transition.direction = "left"
                    user_info = values.val()
                    user_id = user.uid
                    print(user_info)

                else:
                    self.dialog = MDDialog(title="Invalid Login", text="Please confirm your Email Id\nAnd try again", radius=[20, 7, 20, 7])
                    self.dialog.open()

            except Exception as e:
                print(e.args)
                self.dialog = MDDialog(title="Invalid Login", text="Enter correct credentials or signup if you don't have an account", radius=[20, 7, 20, 7])
                self.dialog.open()

        self.ids.user.text = ""
        self.ids.password.text = ""

        self.load()
        self.a = 1

    def signup(self):
        self.ids.user.text = ""
        self.ids.password.text = ""
        self.manager.current = "Register"
        self.manager.transition.direction = "left"

    def reset(self):
        auth1.send_password_reset_email(self.ids.user.text)

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
    l = None

    def back(self):
        self.ids.user.text = ""
        self.ids.password.text = ""
        self.ids.email.text = ""
        self.manager.current = "Login"
        self.manager.transition.direction = "right"

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

    def loader(self):
        self.l = MDDialog(
            size_hint=(None, None),
            size= (0, 0),
            type="custom",
            content_cls=Loader(),
        )
        self.l.open()

    # check unique username
    def username_check(self, name):
        page=auth.list_users()
        users = [user.display_name for  user in page.users]
        if name in users:
            return False
        return True

    def yes(self, inst):
        self.loader()
        threading.Thread(target=self.yess).start()

    def yess(self):
        global user_id
        global user_info

        email = self.ids.email.text
        username = self.ids.user.text
        password= self.ids.password.text

        try:
            if self.username_check(username):
                info = {"username": username, "email": email, "role": self.t, "course":{"name":self.course,"cid":self.c_id},"day":1}
                user = auth.create_user(email =email, password =password, display_name=username)
                login = auth1.sign_in_with_email_and_password(email, password)
                print(user.uid)
                database.child("Users").child("Teacher").child(user.uid).set(info)
                # db.child("Student").child(user.uid).set(data)

                # send email verification1
                auth1.send_email_verification(login['idToken'])
                print("\nPlease verify your email id")
                user_id = user.uid
                user_info = info

                self.d.dismiss()
                self.dialog.dismiss()
                self.ids.btn_tch.icon = "assets/teacher.png"
                self.ids.btn_std.icon == "assets/student.png"
                self.ids.user.text = ""
                self.ids.password.text = ""
                self.ids.email.text = ""
                self.t = 0
                self.l.dismiss()
                self.ids.load.active = False
                self.manager.current = "Login"
                self.manager.transition.direction = "left"
            else:
                self.dialog = MDDialog(title="Invalid SignUp", text="Username already existed", radius=[20, 7, 20, 7])
                self.dialog.open()
                self.a = 0
        except Exception as e:
                self.dialog = MDDialog(title="Invalid SignUp", text="Email already existed", radius=[20, 7, 20, 7])
                self.dialog.open()
                self.a = 0

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
            try:
                if self.username_check(username):
                    info = {"username": username, "email": email, "role": self.t}
                    user = auth.create_user(email =email, password =password, display_name=username)
                    login = auth1.sign_in_with_email_and_password(email, password)
                    print(user.uid)
                    database.child("Users").child("Student").child(user.uid).set(info)

                    #send email verification1
                    auth1.send_email_verification(login['idToken'])
                    print("\nPlease verify your email id")
                    user_id = user.uid
                    user_info = info

                    x = firebase.get("Users/Teacher/",'')
                    for i in x:
                        y =x[i]["course"]["Labs"]
                        for j in y:
                            y[j]["status"]=0
                        database.child("Users").child("Student").child(user_id).child("courses").child(x[i]["course"]["cid"]).child("Labs").set(y)
                        database.child("Users").child("Student").child(user_id).child("courses").child(x[i]["course"]["cid"]).child("Attendence").set(0)
                        z = x[i]["course"]["Assignments"]
                        for k in z:
                            z[k]["status"]=0
                        database.child("Users").child("Student").child(user_id).child("courses").child(x[i]["course"]["cid"]).child("Assignments").set(z)

                    self.ids.btn_tch.icon = "assets/teacher.png"
                    self.ids.btn_std.icon == "assets/student.png"
                    self.ids.user.text = ""
                    self.ids.password.text = ""
                    self.ids.email.text = ""
                    self.t = 0
                    self.ids.load.active = False
                    self.manager.current = "Login"
                    self.manager.transition.direction = "left"
                else:
                    self.dialog = MDDialog(title="Invalid SignUp", text="Username already existed", radius=[20, 7, 20, 7])
                    self.dialog.open()
                    self.a = 0
            except Exception as e:
                self.dialog = MDDialog(title="Invalid SignUp", text="Email already existed", radius=[20, 7, 20, 7])
                self.dialog.open()
                self.a = 0

        self.ids.load.active = False
        self.a = 1

class Tdashboard(Screen):
    loader = None
    def __init__(self,**kwargs):
        super(Tdashboard,self).__init__(**kwargs)

    def load(self):
        self.loader = MDDialog(
            size_hint=(None, None),
            size= (0, 0),
            type="custom",
            content_cls=Loader(),
        )
        self.loader.open()
    def add_stds(self):
        self.ids.student_list.clear_widgets()
        x = firebase.get("Users/Student",'')
        for i in x:
            card = MDCard(orientation='vertical',size_hint=(None,None),size=(390,60),border_radius=10,radius=[10],md_bg_color=[54/255, 154/255, 230/255,0.5],elevation=0)
            std_name  = MDLabel(text=x[i]["username"],font_style="H5",bold=True,halign="center")
            card.add_widget(std_name)
            self.ids.student_list.add_widget(card)

    def on_enter(self,*args):
        self.load()
        threading.Thread(target=self.spin).start()

    def spin(self):
        try:
            import datetime
            now = datetime.datetime.now()
            d = str(now.strftime("%A"))
            self.ids.uname.text = "Hello "+str(user_info["username"])
            self.ids.label.text = "An investment in knowledge pays best interest"
            self.ids.day.text = d
            self.ids.nowcard.md_bg_color = [255/255, 204/255, 104/255, 0.5]
            self.ids.nowlabel.text = "Now"
            self.ids.nowlabel.color = [1, 105/255, 5/255]
            self.add_stds()
            self.ids.lab_c.text= str(len(firebase.get("Users/Teacher/"+user_id+"/course/Labs",'')))
            self.ids.ass_c.text= str(len(firebase.get("Users/Teacher/"+user_id+"/course/Assignments",'')))
            # add student cards to MDboxlayout( id = student_list)
            self.loader.dismiss()
        except:
            pass

class Sdashboard(Screen):
    loader = None
    def __init__(self,**kwargs):
        super(Sdashboard,self).__init__(**kwargs)

    def open_scourse(self,i):
        print(i)
    def l_a_count(self):
        self.ids.today.clear_widgets()
        self.ids.tomorrow.clear_widgets()
        x = firebase.get("Users/Student/"+user_id+"/courses",'')
        l_c = 0
        a_c = 0
        for i in x:
            y = x[i]["Labs"]
            for j in y:
                if (y[j]["status"]==0):
                    l_c=l_c+1
                    if (int((y[j]["deadline"].split("-"))[0])==datetime.now().day):
                        card = MDCard(orientation='horizontal',size_hint=(None,None),size=(380,80),pos_hint={'center_x':0.5 , 'center_y':0.5},elevation=0,md_bg_color=[184/255, 226/255, 1, 1],border_radius=10,radius=[10],padding=10,on_release=lambda f:self.open_scourse(str(i)))
                        card_l = MDBoxLayout(orientation='vertical')
                        title = MDLabel(text=y[j]["title"],font_style="H5",bold=True,color=[7/255, 12/255, 173/255])
                        course = MDLabel(text=str(i),font_style="H6",bold=True,color=[7/255, 12/255, 173/255])
                        time_left = MDLabel(text=str(24-datetime.now().hour)+" hours left",font_style="H6")
                        card_l.add_widget(title)
                        card_l.add_widget(course)
                        card.add_widget(card_l)
                        card.add_widget(time_left)
                        self.ids.today.add_widget(card)
                    elif (int((y[j]["deadline"].split("-"))[0])==int(datetime.now().day)+1):
                        card = MDCard(orientation='horizontal',size_hint=(None,None),size=(380,80),pos_hint={'center_x':0.5 , 'center_y':0.5},elevation=0,md_bg_color=[184/255, 226/255, 1, 1],border_radius=10,radius=[10],padding=10)
                        card_l = MDBoxLayout(orientation='vertical')
                        title = MDLabel(text=y[j]["title"],font_style="H5",bold=True,color=[7/255, 12/255, 173/255])
                        course = MDLabel(text=str(i),font_style="H6",bold=True,color=[7/255, 12/255, 173/255])
                        time_left = MDLabel(text=str(24-datetime.now().hour+24)+" hours left",font_style="H6")
                        card_l.add_widget(title)
                        card_l.add_widget(course)
                        card.add_widget(card_l)
                        card.add_widget(time_left)
                        self.ids.tomorrow.add_widget(card)
            z = x[i]["Assignments"]
            for k in z:
                if (z[k]["status"]==0):
                    a_c=a_c+1
                    if (int((z[k]["deadline"].split("-"))[0])==datetime.now().day):
                        card = MDCard(orientation='horizontal',size_hint=(None,None),size=(380,80),pos_hint={'center_x':0.5 , 'center_y':0.5},elevation=0,md_bg_color=[255/255, 204/255, 104/255, 0.5],border_radius=10,radius=[10],padding=10)
                        card_l = MDBoxLayout(orientation='vertical')
                        title = MDLabel(text=z[k]["title"],font_style="H5",bold=True,color=[7/255, 12/255, 173/255])
                        course = MDLabel(text=str(i),font_style="H6",bold=True,color=[7/255, 12/255, 173/255])
                        time_left = MDLabel(text=str(24-datetime.now().hour)+" hours left",font_style="H6")
                        card_l.add_widget(title)
                        card_l.add_widget(course)
                        card.add_widget(card_l)
                        card.add_widget(time_left)
                        self.ids.today.add_widget(card)
                    elif (int((z[k]["deadline"].split("-"))[0])==int(datetime.now().day)+1):
                        card = MDCard(orientation='horizontal',size_hint=(None,None),size=(380,80),pos_hint={'center_x':0.5 , 'center_y':0.5},elevation=0,md_bg_color=[184/255, 226/255, 1, 1],border_radius=10,radius=[10],padding=10)
                        card_l = MDBoxLayout(orientation='vertical')
                        title = MDLabel(text=z[k]["title"],font_style="H5",bold=True,color=[7/255, 12/255, 173/255])
                        course = MDLabel(text=str(i),font_style="H6",bold=True,color=[7/255, 12/255, 173/255])
                        time_left = MDLabel(text=str(24-datetime.now().hour+24)+" hours left",font_style="H6")
                        card_l.add_widget(title)
                        card_l.add_widget(course)
                        card.add_widget(card_l)
                        card.add_widget(time_left)
                        self.ids.tomorrow.add_widget(card)
        self.ids.l_c.text=str(l_c)
        self.ids.a_c.text=str(a_c)

    def load(self):
        self.loader = MDDialog(
            size_hint=(None, None),
            size= (0, 0),
            type="custom",
            content_cls=Loader(),
        )
        self.loader.open()

    def spin(self):
        try:
            import datetime
            now = datetime.datetime.now()
            d = str(now.strftime("%A"))
            self.ids.uname.text = "Hello "+str(user_info["username"])
            self.ids.day.text = d
            self.ids.label.text = "An investment in knowledge pays best interest"
            self.l_a_count()
            self.loader.dismiss()
        except:
            pass

    def on_enter(self,*args):
        self.load()
        threading.Thread(target=self.spin).start()

class ClockLabel(Label):
    def __init__(self,**kwargs):
        super(ClockLabel,self).__init__(**kwargs)
        Clock.schedule_interval(self.update,1)
    def update(self,*args):
        self.text= f"{datetime.now().strftime('%H:%M')}"

class Ticon(MDIconButton):
    def __init__(self, **kwargs):
        try:
            super(Ticon,self).__init__(**kwargs)
            Clock.schedule_interval(self.update_class_icon,0.3)
        except:
            pass
    def update_class_icon(self,*args):
        try:
            tt()
            u = user_info["course"]["name"]
            n = now_next[0]["name"]
            if(str(u.split()[0]).lower() == str(n.split()[0]).lower()):
                self.icon=now_next[0]["pic"]
                self.screen = "Tcourse"
            else:
                self.icon="assets/male.png"
                self.screen = "Tdashboard"
        except:
            pass

class Ttext(MDTextButton):
    def __init__(self, **kwargs):
        try:
            super(Ttext,self).__init__(**kwargs)
            Clock.schedule_interval(self.update_class_icon,0.3)
        except:
            pass
    def update_class_icon(self,*args):
        try:
            tt()
            u = user_info["course"]["name"]
            n = now_next[0]["name"]
            if(str(u.split()[0]).lower() == str(n.split()[0]).lower()):
                self.text=now_next[0]["name"]
                self.screen = "Tcourse"
            else:
                self.text="There is no class today"
                self.screen = "Tdashboard"
        except:
            pass

class NowIcon(MDIconButton):
    def __init__(self, **kwargs):
        super(NowIcon,self).__init__(**kwargs)
        Clock.schedule_interval(self.update_class_icon,5)
    def update_class_icon(self,*args):
        tt()
        self.icon=now_next[0]["pic"]

    def course(self):
        course1 = now_next[0]["name"]
        c1_id = now_next[0]["cid"]
        self.screen = now_next[0]["screen"]

class NowText(MDTextButton):
    def __init__(self, **kwargs):
        super(NowText,self).__init__(**kwargs)
        Clock.schedule_interval(self.update_class_text,5)

    def update_class_text(self,*args):
        tt()
        self.text=now_next[0]["name"]

    def course(self):
        global c1_id
        global course1
        course1 = now_next[0]["name"]
        c1_id = now_next[0]["cid"]
        self.screen = now_next[0]["screen"]

class NextIcon(MDIconButton):
    def __init__(self, **kwargs):
        super(NextIcon,self).__init__(**kwargs)
        Clock.schedule_interval(self.update_class_icon,5)
    def update_class_icon(self,*args):
        tt()
        self.icon=now_next[1]["pic"]

    def course(self):
        course1 = now_next[1]["name"]
        c1_id = now_next[1]["cid"]
        self.screen = now_next[1]["screen"]

class NextText(MDTextButton):
    def __init__(self, **kwargs):
        super(NextText,self).__init__(**kwargs)
        Clock.schedule_interval(self.update_class_text,5)
    def update_class_text(self,*args):
        tt()
        self.text=now_next[1]["name"]

    def course(self):
        course1 = now_next[1]["name"]
        c1_id = now_next[1]["cid"]
        self.screen = now_next[1]["screen"]

class TodayDate(MDLabel):
    def __init__(self, **kwargs):
        super(TodayDate,self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 5)
    def update(self,*args):
        self.text=str(datetime.now().day)+"-"+str(datetime.now().month)+"-"+str(datetime.now().year)

class Scourse(Screen):
    def ai(self):
        global c1_id
        c1_id = "AI"
        self.manager.current = "Scourse1"
        self.manager.transition.direction = "left"
    def sepm(self):
        global c1_id
        c1_id = "SEPM"
        self.manager.current = "Scourse1"
        self.manager.transition.direction = "left"
    def cf(self):
        global c1_id
        c1_id = "CF"
        self.manager.current = "Scourse1"
        self.manager.transition.direction = "left"
    def dsp(self):
        global c1_id
        course1 = "Software Engineering And Project Management"
        c1_id = "SEPM"
        self.manager.current = "Scourse1"
        self.manager.transition.direction = "left"
    def cf(self):
        global c1_id
        course1 = "Computer Forensics"
        c1_id = "CF"
        self.manager.current = "Scourse1"
        self.manager.transition.direction = "left"
    def dsp(self):
        global c1_id
        course1 = "Digital Signal Processing"
        c1_id = "DSP"
        self.manager.current = "Scourse1"
        self.manager.transition.direction = "left"
    def sc(self):
        global c1_id
        c1_id = "SC"
        self.manager.current = "Scourse1"
        self.manager.transition.direction = "left"
    def hrm(self):
        global c1_id
        course1 = "Soft Computing"
        c1_id = "SC"
        self.manager.current = "Scourse1"
        self.manager.transition.direction = "left"
    def hrm(self):
        global c1_id
        course1 = "Human Resource Management"
        c1_id = "HRM"
        self.manager.current = "Scourse1"
        self.manager.transition.direction = "left"
    def fma(self):
        global c1_id
        course1 = "Financial Management & Accounting"
        c1_id = "FMA"
        self.manager.current = "Scourse1"
        self.manager.transition.direction = "left"
    def osm(self):
        global c1_id
        course1 = "Operations & Supply Chain Management"
        c1_id = "OSM"
        self.manager.current = "Scourse1"
        self.manager.transition.direction = "left"

class Tcourse(Screen):

    dialog = None
    file_manager = None
    dialog1 = None
    p = ""
    loader = None

    def __init__(self, **kw):
        super(Tcourse, self).__init__(**kw)
        # Clock.schedule_interval(self.on_enter,5)

    def joinclass(self):
        webbrowser.open('https://meet.google.com/jpq-webf-iwy?pli=1', new = 1)

    def load(self):
        self.loader = MDDialog(
            size_hint=(None, None),
            size= (0,0),
            type="custom",
            content_cls=Loader(),
        )
        self.loader.open()

    def attendence_cal(self):
        link = database.child("Users").child("Teacher").child(user_id).child("course").child("link").get().val()
        link = link.replace(link.split("/")[-1],"export?format=csv")
        course = user_info["course"]["cid"]
        df = pd.read_csv(link)
        students = database.child('Users').child('Student').get().val()
        day = int(database.child('Users').child("Teacher").child(user_id).child('day').get().val())
        for i in students:
            try:
                attendence = int(database.child('Users').child('Student').child(i).child('courses').child(course).child('Attendence').get().val())
                name = database.child('Users').child('Student').child(i).child('username').get().val()
                if df[df['First Name']==name]['Present'].values[0] == 'Y':
                    attendence=(attendence+1)
                database.child('Users').child('Student').child(i).child('courses').child(course).child('Attendence').set(attendence)
            except Exception as e:
                pass
        day+=1
        database.child('Users').child('Teacher').child(user_id).child('day').set(day)

    def attendence(self):
        if (database.child("Users").child("Teacher").child(user_id).child("course").child("link").get().val()==None):
            self.dialog = MDDialog(
                title="ADD Link",
                type="custom",
                content_cls=Attend_link(),
                buttons=[
                    MDFlatButton(text="CANCEL", on_press = self.cancel),
                    MDFlatButton(text="OK", on_press = self.att_link),
                ],
            )
            self.dialog.open()
        else:
            self.attendence_cal()

    def att_link(self,inst):
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                database.child("Users").child("Teacher").child(user_id).child("course").child("link").set(obj.text)
                self.attendence_cal()
        self.dialog.dismiss()

    def lab_load(self, inst):
        self.load()
        threading.Thread(target=self.lab_ok).start()

    def ass_load(self, inst):
        self.load()
        threading.Thread(target=self.assign_ok).start()

    def notes_load(self, inst):
        self.load()
        threading.Thread(target=self.yes).start()

    def addlab(self):
        self.dialog = MDDialog(
            title="ADD LAB",
            type="custom",
            content_cls=Lab(),
            buttons=[
                MDFlatButton(text="CANCEL", on_press = self.cancel),
                MDFlatButton(text="OK", on_press = self.lab_load),
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
                MDFlatButton(text="OK", on_press = self.ass_load),
            ],
        )
        self.dialog.open()

    def addnotes(self):
        self.file_manager = MDFileManager(
            select_path = self.select_path,
            exit_manager = self.exit_manager,
        )
        self.file_manager.show('\\Users\\'+current_user)

    def no(self, inst):
        self.dialog1.dismiss()

    def yes(self):
        n = self.p
        n = n.split('\\')

        # Name of the file that should be displayed in Tcourse
        name = n.pop()
        self.dialog1.dismiss()

        # self.p is the path of the file
        self.p = "C:"+self.p

        storage.child(user_info['course']['cid']+name).put(self.p)
        pdf_url=storage.child(user_info['course']['cid']+name).get_url(None)
        firebase.post("Courses/"+user_info["course"]["cid"]+"/",{"url":pdf_url,"title":name})

        self.loader.dismiss()
        self.file_manager.close()
        self.add_note_card()
        Snackbar(text="File Successfully uploaded -_- ",snackbar_x="10dp",snackbar_y="10dp",size_hint_x=0.5,pos_hint={'center_x': 0.5, 'center_y': 0.1}).open()

    def open_notes(self,link):
        webbrowser.open(link,new=1)

    def add_note_card(self):
        self.ids.tnotes.clear_widgets()
        x= firebase.get("Courses/"+user_info["course"]["cid"],'')
        c = 1
        for i in x:
            card = MDCard(orientation='horizontal',size_hint=(None,None),size=(880,40),border_radius=10,radius=[10],elevation=0,padding=10,md_bg_color=[84/255,255/255,103/255,1],on_release=lambda f:self.open_notes(x[i]["url"]))
            card_title = MDLabel(text=str(c)+". "+x[i]["title"],font_style="H5")
            card.add_widget(card_title)
            c = c+1
            self.ids.tnotes.add_widget(card)

    def select_path(self, path):
        self.p = path
        self.dialog1 = MDDialog(
            title="Confirm ?",
            text = "Are you sure you want to upload this file",
            buttons=[
                MDFlatButton(text="NO", on_press = self.no),
                MDFlatButton(text="YES", on_press = self.notes_load),
            ],
        )
        self.dialog1.open()


    def exit_manager(self, *args):
        self.file_manager.close()

    def view_files(self,part):
        global part_type
        part_type = part
        self.manager.current = "Tstudentfiles"
        self.manager.transition.direction = "up"

    def lab_ok(self):
        regex = r'[\s]*'
        a = 0
        list = []
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                list.append(obj.text)
        list.reverse()

        for i in list:
            if(re.fullmatch(regex, i)):
                self.loader.dismiss()
                time.sleep(0.5)
                self.d = MDDialog(title = "Invalid Input", text = "Field must not be empty")
                self.d.open()
                a = 1
                break

        if(a == 0):
            for i in firebase.get("Users/Student",''):
                firebase.post("Users/Student/"+i+"/courses/"+user_info["course"]["cid"]+"/Labs",{"title":list[0],"question":list[1],"deadline":list[2],"post_time":str(datetime.now().day)+"-"+str(datetime.now().month)+"-"+str(datetime.now().year)+"  "+str(datetime.now().hour)+"-"+str(datetime.now().minute)+"-"+str(datetime.now().second),"status":0})
            firebase.post("Users/Teacher/"+user_id+"/course/Labs",{"title":list[0],"question":list[1],"deadline":list[2],"post_time":str(datetime.now().day)+"-"+str(datetime.now().month)+"-"+str(datetime.now().year)+"  "+str(datetime.now().hour)+"-"+str(datetime.now().minute)+"-"+str(datetime.now().second)})

            self.loader.dismiss()
            self.dialog.dismiss()
            Snackbar(text="Lab Successfully posted -_- ",snackbar_x="10dp",snackbar_y="10dp",size_hint_x=0.5,pos_hint={'center_x': 0.5, 'center_y': 0.1}).open()
            self.add_labcard()

    def add_labcard(self):
        self.ids.tlab.clear_widgets()
        x = firebase.get("Users/Teacher/"+user_id+"/course/Labs",'')
        for i in x:
            if (database.child("Users").child("Teacher").child(user_id).child("course").child("Labs").child(i).child("student_files").get().val()==None):
                nfs = "0"
            else:
                nfs= str(len(x[i]["student_files"]))
            card = MDCard(orientation='horizontal',size_hint=(None,None),size=(880,60),border_radius=10,radius=[10],elevation=0,padding=10,md_bg_color=[84/255,255/255,103/255,1],on_release=lambda f:self.view_files("Labs"))
            card_l = MDBoxLayout(orientation='vertical')
            card_l_title = MDLabel(text=x[i]["title"],font_style="H6",bold=True)
            card_l_question = MDLabel(text=x[i]["question"])
            card_r_deadline = MDLabel(text=x[i]["deadline"],bold=True)
            card_nfs = MDLabel(text="Submissions : "+nfs,font_style="H6",bold=True)
            card_r = MDBoxLayout(orientation='vertical')
            card_l.add_widget(card_l_title)
            card_l.add_widget(card_l_question)
            card.add_widget(card_l)
            card_r.add_widget(card_r_deadline)
            card_r.add_widget(card_nfs)
            card.add_widget(card_r)
            self.ids.tlab.add_widget(card)

    def assign_ok(self):
        regex = r'[\s]*'
        a = 0
        list = []
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                list.append(obj.text)
        list.reverse()

        for i in list:
            if(re.fullmatch(regex, i)):
                self.loader.dismiss()
                time.sleep(0.5)
                self.d = MDDialog(title = "Invalid Input", text = "Field must not be empty")
                self.d.open()
                a = 1
                break

        if(a == 0):

            for i in firebase.get("Users/Student",''):
                firebase.post("Users/Student/"+i+"/courses/"+user_info["course"]["cid"]+"/Assignments",{"title":list[0],"question":list[1],"deadline":list[2],"post_time":str(datetime.now().day)+"-"+str(datetime.now().month)+"-"+str(datetime.now().year)+"  "+str(datetime.now().hour)+"-"+str(datetime.now().minute)+"-"+str(datetime.now().second),"status":0})
            firebase.post("Users/Teacher/"+user_id+"/course/Assignments",{"title":list[0],"question":list[1],"deadline":list[2],"post_time":str(datetime.now().day)+"-"+str(datetime.now().month)+"-"+str(datetime.now().year)+"  "+str(datetime.now().hour)+"-"+str(datetime.now().minute)+"-"+str(datetime.now().second)})

            self.loader.dismiss()
            self.dialog.dismiss()
            Snackbar(text="Assignment Successfully posted -_- ",snackbar_x="10dp",snackbar_y="10dp",size_hint_x=0.5,pos_hint={'center_x': 0.5, 'center_y': 0.1}).open()
            self.add_asscard()

    def add_asscard(self):
        self.ids.tassignment.clear_widgets()
        x = firebase.get("Users/Teacher/"+user_id+"/course/Assignments",'')
        for i in x:
            if (database.child("Users").child("Teacher").child(user_id).child("course").child("Assignments").child(i).child("student_files").get().val()==None):
                nfs = "0"
            else:
                nfs= str(len(x[i]["student_files"]))
            card = MDCard(orientation='horizontal',size_hint=(None,None),size=(880,60),border_radius=10,radius=[10],elevation=0,padding=10,md_bg_color=[84/255,255/255,103/255,1])
            card_l = MDBoxLayout(orientation='vertical')
            card_l_title = MDLabel(text=x[i]["title"],font_style="H6",bold=True)
            card_l_question = MDLabel(text=x[i]["question"])
            card_r_deadline = MDLabel(text=x[i]["deadline"],bold=True)
            card_nfs = MDLabel(text="Submissions : "+nfs,font_style="H6",bold=True)
            card_r = MDBoxLayout(orientation='vertical')
            card_l.add_widget(card_l_title)
            card_l.add_widget(card_l_question)
            card.add_widget(card_l)
            card_r.add_widget(card_r_deadline)
            card_r.add_widget(card_nfs)
            card.add_widget(card_r)
            self.ids.tassignment.add_widget(card)

    def cancel(self, inst):
        self.dialog.dismiss()

    def on_enter(self, *args):
        self.load()
        threading.Thread(target=self.spin).start()

    def spin(self):
        self.ids.tname.text = 'Dr. ' + user_info["username"]
        self.ids.tmail.text = user_info["email"]
        try:
            self.add_labcard()
            self.add_asscard()
            self.add_note_card()
            self.loader.dismiss()
        except:
            pass

class Lab(MDBoxLayout):
    pass
class Slab_title(MDBoxLayout):
    pass
class Assignment(MDBoxLayout):
    pass
class Attend_link(MDBoxLayout):
    pass
class Sass_title(MDBoxLayout):
    pass
class Loader(MDBoxLayout):
    pass

class Sevent(Screen):
    loader = None
    def load(self):
        self.loader = MDDialog(
            size_hint=(None, None),
            size= (0, 0),
            type="custom",
            content_cls=Loader(),
        )
        self.loader.open()

    def spin(self):
        try:
            self.events_count()
            self.loader.dismiss()
        except:
            pass
    def on_enter(self, *args):
        self.load()
        threading.Thread(target=self.spin).start()

    def events_count(self):
        x = firebase.get("Users/Student/"+user_id+"/courses",'')
        for i in x:
            y = x[i]["Labs"]
            for j in sorted(y,key=lambda j:(y[j]["deadline"]).split("-")[0],reverse=False):
                card = MDCard(orientation='horizontal',size_hint=(None,None),size=(800,60),pos_hint={'center_x':0.5 , 'center_y':0.5},elevation=0,md_bg_color=[184/255, 226/255, 1, 1],border_radius=10,radius=[10],padding=10)
                title = MDLabel(text=y[j]["title"],font_style="H5",bold=True,color=[7/255, 12/255, 173/255])
                course = MDLabel(text=str(i),font_style="H6",bold=True,color=[7/255, 12/255, 173/255])
                card.add_widget(title)
                card.add_widget(course)
                if y[j]["status"] == 1 :
                    card_icon = MDIconButton(icon = "check",user_font_size = "36dp")
                    card.add_widget(card_icon)
                self.ids.slab.add_widget(card)
        for i in x:
            z = x[i]["Assignments"]
            for j in sorted(z,key=lambda j:(z[j]["deadline"]).split("-")[0],reverse=False):
                card = MDCard(orientation='horizontal',size_hint=(None,None),size=(800,60),pos_hint={'center_x':0.5 , 'center_y':0.5},elevation=0,md_bg_color=[184/255, 226/255, 1, 1],border_radius=10,radius=[10],padding=10)
                title = MDLabel(text=z[j]["title"],font_style="H5",bold=True,color=[7/255, 12/255, 173/255])
                course = MDLabel(text=str(i),font_style="H6",bold=True,color=[7/255, 12/255, 173/255])
                card.add_widget(title)
                card.add_widget(course)
                if z[j]["status"] == 1 :
                    card_icon = MDIconButton(icon = "check",user_font_size = "36dp")
                    card.add_widget(card_icon)
                self.ids.sassignment.add_widget(card)

class Tevent(Screen):
    loader = None
    def load(self):
        self.loader = MDDialog(
            size_hint=(None, None),
            size= (0, 0),
            type="custom",
            content_cls=Loader(),
        )
        self.loader.open()

    def spin(self):
        try:
            self.add_labcard()
            self.add_asscard()
            self.loader.dismiss()
        except:
            pass
    def on_enter(self, *args):
        self.load()
        threading.Thread(target=self.spin).start()

    def add_labcard(self):
        # add lab cards
        self.ids.tlab.clear_widgets()
        x = firebase.get("Users/Teacher/"+user_id+"/course/Labs",'')
        for i in x:
            card = MDCard(orientation='horizontal',size_hint=(None,None),size=(880,100),border_radius=10,radius=[10],elevation=0,padding=10,md_bg_color=[84/255,255/255,103/255,1])
            card_l = MDBoxLayout(orientation='vertical')
            card_l_title = MDLabel(text=x[i]["title"],font_style="H6",bold=True)
            card_l_question = MDLabel(text=x[i]["question"])
            card_r_deadline = MDLabel(text="Deadline : "+x[i]["deadline"],bold=True)

            card_r = MDBoxLayout(orientation='vertical')
            card_l.add_widget(card_l_title)
            card_l.add_widget(card_l_question)
            card.add_widget(card_l)
            card_r.add_widget(card_r_deadline)
            card.add_widget(card_r)
            self.ids.tlab.add_widget(card)

    def add_asscard(self):
        # add assignment cards
        self.ids.tassignment.clear_widgets()
        x = firebase.get("Users/Teacher/"+user_id+"/course/Assignments",'')
        for i in x:
            card = MDCard(orientation='horizontal',size_hint=(None,None),size=(880,100),border_radius=10,radius=[10],elevation=0,padding=10,md_bg_color=[84/255,255/255,103/255,1])
            card_l = MDBoxLayout(orientation='vertical')
            card_l_title = MDLabel(text=x[i]["title"],font_style="H6",bold=True)
            card_l_question = MDLabel(text=x[i]["question"])
            card_r_deadline = MDLabel(text="Deadline : "+x[i]["deadline"],bold=True)

            card_r = MDBoxLayout(orientation='vertical')
            card_l.add_widget(card_l_title)
            card_l.add_widget(card_l_question)
            card.add_widget(card_l)
            card_r.add_widget(card_r_deadline)
            card.add_widget(card_r)
            self.ids.tassignment.add_widget(card)


class Schat(Screen):

    loader = None
    def __init__(self, **kw):
        super(Schat, self).__init__(**kw)
        # Clock.schedule_interval(self.on_enter,5)

    def send(self):
        regex = r'[\s]*'
        txt = self.ids.message.text
        if(re.fullmatch(regex,txt)):
            MDDialog(title = "Invalid", text = "Field must not be empty").open()
            self.ids.message.text= ""
        else:
            firebase.post("Schat",{"message":txt,"sender":user_info["username"],"time":str(datetime.now().day)+"-"+str(datetime.now().month)+"-"+str(datetime.now().year)+"  "+str(datetime.now().hour)+":"+str(datetime.now().minute)})
            self.ids.message.text = ""
            self.add_cards()

    def add_cards(self):
        self.ids.other.clear_widgets()
        self.ids.user.clear_widgets()
        x = firebase.get("Schat/",'')
        for i in x:
            if (x[i]["sender"]==user_info["username"]):
                card_empty = MDLabel(size_hint=(None,None),size=(300,100), pos_hint={'center_x':.5 , 'center_y':.5})
                self.ids.other.add_widget(card_empty)
                card = MDCard(orientation='vertical',size_hint=(None,None),size=(480,100), radius=[30, 0, 30, 15],elevation=17,padding=20,md_bg_color=[8/255, 1, 98/255, 0.5], pos_hint={'center_x':.5 , 'center_y':.5})
                card_nt = MDBoxLayout(orientation='horizontal', size_hint_y=0.1)
                card_name = MDLabel(text="You",font_style = "H6")
                card_time = MDLabel(text=x[i]["time"],bold=True)
                empty = MDLabel(size_hint_x=0.8)
                card_nt.add_widget(card_name)
                card_nt.add_widget(empty)
                card_nt.add_widget(card_time)
                card_message = MDLabel(text=x[i]["message"],font_size=(20))
                card.add_widget(card_nt)
                card.add_widget(card_message)
                self.ids.user.add_widget(card)
            else:
                card_empty = MDLabel(size_hint=(None,None),size=(300,100), pos_hint={'center_x':.5 , 'center_y':.5})
                self.ids.user.add_widget(card_empty)
                card = MDCard(orientation='vertical',size_hint=(None,None),size=(480,100), radius=[0,30,15,30],elevation=17,padding=20,md_bg_color=[54/255, 154/255, 230/255,0.5],pos_hint={'center_x':.5 , 'center_y':.5})
                card_nt = MDBoxLayout(orientation='horizontal', size_hint_y=0.1)
                card_name = MDLabel(text=x[i]["sender"],font_style = "H6")
                card_time = MDLabel(text=x[i]["time"],bold=True)
                empty = MDLabel(size_hint_x=0.8)
                card_nt.add_widget(card_name)
                card_nt.add_widget(empty)
                card_nt.add_widget(card_time)
                card_message = MDLabel(text=x[i]["message"],font_size=(20))
                card.add_widget(card_nt)
                card.add_widget(card_message)
                self.ids.other.add_widget(card)

    def on_enter(self, *args):
        self.load()
        threading.Thread(target=self.spin).start()

    def spin(self):
        try:
            self.add_cards()
            self.loader.dismiss()
        except:
            pass

    def load(self):
        self.loader = MDDialog(
            size_hint=(None, None),
            size= (0, 0),
            type="custom",
            content_cls=Loader(),
        )
        self.loader.open()

    def clear(self):
        self.ids.other.clear_widgets()
        self.ids.user.clear_widgets()
        self.ids.message.text = ""


class Tchat(Screen):

    loader = None
    def __init__(self, **kw):
        super(Tchat, self).__init__(**kw)
        # Clock.schedule_interval(self.on_enter,5)

    def send(self):
        regex = r'[\s]*'
        txt = self.ids.message.text
        if(re.fullmatch(regex,txt)):
            MDDialog(title = "Invalid", text = "Field must not be empty").open()
            self.ids.message.text= ""
        else:
            firebase.post("Tchat",{"message":txt,"sender":user_info["username"],"time":str(datetime.now().day)+"-"+str(datetime.now().month)+"-"+str(datetime.now().year)+"  "+str(datetime.now().hour)+":"+str(datetime.now().minute),"course":firebase.get("/Users/Teacher/"+user_id+"/", 'course/cid')})
            self.ids.message.text = ""
            self.add_cards()

    def add_cards(self):
        self.ids.other.clear_widgets()
        self.ids.user.clear_widgets()
        x = firebase.get("Tchat/",'')
        for i in x:
            if (x[i]["sender"]==user_info["username"]):
                card_empty = MDLabel(size_hint=(None,None),size=(300,100), pos_hint={'center_x':.5 , 'center_y':.5})
                self.ids.other.add_widget(card_empty)
                card = MDCard(orientation='vertical',size_hint=(None,None),size=(480,100), radius=[30, 0, 30, 15],elevation=17,padding=20,md_bg_color=[8/255, 1, 98/255, 0.5], pos_hint={'center_x':.5 , 'center_y':.5})
                card_nt = MDBoxLayout(orientation='horizontal', size_hint_y=0.1)
                card_name = MDLabel(text="You",font_style = "H6")
                card_time = MDLabel(text=x[i]["time"],bold=True)
                empty = MDLabel(size_hint_x=0.8)
                card_nt.add_widget(card_name)
                card_nt.add_widget(empty)
                card_nt.add_widget(card_time)
                card_message = MDLabel(text=x[i]["message"],font_size=(20))
                card.add_widget(card_nt)
                card.add_widget(card_message)
                self.ids.user.add_widget(card)
            else:
                card_empty = MDLabel(size_hint=(None,None),size=(300,100), pos_hint={'center_x':.5 , 'center_y':.5})
                self.ids.user.add_widget(card_empty)
                card = MDCard(orientation='vertical',size_hint=(None,None),size=(480,100), radius=[0,30,15,30], elevation=17,padding=20,md_bg_color=[54/255, 154/255, 230/255,0.5], pos_hint={'center_x':.5 , 'center_y':.5})
                card_nt = MDBoxLayout(orientation='horizontal', size_hint_y=0.1)
                card_name = MDLabel(text='Dr. '+x[i]["sender"]+'@'+x[i]["course"],font_style = "H6")
                card_time = MDLabel(text=x[i]["time"],bold=True)
                empty = MDLabel(size_hint_x=0.8)
                card_nt.add_widget(card_name)
                card_nt.add_widget(empty)
                card_nt.add_widget(card_time)
                card_message = MDLabel(text=x[i]["message"],font_size=(20))
                card.add_widget(card_nt)
                card.add_widget(card_message)
                self.ids.other.add_widget(card)

    def on_enter(self, *args):
        self.load()
        threading.Thread(target=self.spin).start()

    def spin(self):
        try:
            self.add_cards()
            self.loader.dismiss()
        except:
            pass

    def load(self):
        self.loader = MDDialog(
            size_hint=(None, None),
            size= (0, 0),
            type="custom",
            content_cls=Loader(),
        )
        self.loader.open()

    def clear(self):
        self.ids.other.clear_widgets()
        self.ids.user.clear_widgets()
        self.ids.message.text = ""


class Stimetable(Screen):
    pass
class Ttimetable(Screen):
    pass
class Sannouncement(Screen):
    loader = None
    def __init__(self, **kw):
        super(Sannouncement,self).__init__(**kw)
        # Clock.schedule_interval(self.on_enter,5)
    def load(self):
        self.loader = MDDialog(
            size_hint=(None, None),
            size= (0, 0),
            type="custom",
            content_cls=Loader(),
        )
        self.loader.open()
    def spin(self):
        try:
            self.add_announcements()
            self.loader.dismiss()
        except:
            pass
    def add_announcements(self):
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

    def on_enter(self,*args):
        self.load()
        threading.Thread(target=self.spin).start()

class Tannouncement(Screen):
    loader = None
    def load(self):
        self.loader = MDDialog(
            size_hint=(None, None),
            size= (0, 0),
            type="custom",
            content_cls=Loader(),
        )
        self.loader.open()

    def spin(self):
        try:
            self.add_announcements()
            self.loader.dismiss()
        except:
            pass

    def on_enter(self, *args):
        self.load()
        threading.Thread(target=self.spin).start()

    def announcement_send(self):
        txt=self.ids.Announcemnet_txt.text
        regex = r'[\s]*'

        if(re.fullmatch(regex,txt)):
            MDDialog(title = "Invalid", text = "Field must not be empty").open()
            self.ids.Announcemnet_txt.text= ''
        else:
            firebase.post("Announcements",{"message":txt,"sender":user_info["username"],"time":str(datetime.now().day)+"-"+str(datetime.now().month)+"-"+str(datetime.now().year)+"  "+str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second),"course":firebase.get("/Users/Teacher/"+user_id+"/", 'course/cid')})
            Snackbar(
                text="Announcement Successfully posted -_- ",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=0.5,
                pos_hint={'center_x': 0.5, 'center_y': 0.1}
            ).open()
            self.ids.Announcemnet_txt.text= ''
            self.add_announcements()

    def add_announcements(self):
        self.ids.tannouncement_card.clear_widgets()
        x = firebase.get("Announcements/",'')
        for i in reversed(x):
            if (x[i]["sender"]==user_info["username"]):
                card = MDCard(orientation='vertical',pos_hint={'center_x':.5 , 'center_y':.7},size_hint=(None, None),size=(780,80),border_radius=10,radius=[10],md_bg_color=[184/255,255/255,203/255,1],padding=10,elevation=0)
                icon = MDIconButton(icon='assets/'+x[i]["course"]+'.png',user_font_size=(36),pos_hint={'center_x':.5 , 'center_y':.5})
                space = MDLabel(size_hint_x=0.05)
                card_nt = MDBoxLayout(orientation='horizontal',pos_hint={'center_x':0.5 , 'center_y': 1},size_hint_y=0.001,spacing=50)
                card_name = MDLabel(text='Dr. '+x[i]["sender"]+'@'+x[i]["course"],font_style = "H6",size_hint_y=0.001)
                card_time = MDLabel(text=x[i]["time"],size_hint_y=0.001,size_hint_x = 0.6, bold=True, pos_hint={'center_x':0.8 , 'center_y':0.1})
                card_empty = MDLabel(size_hint_x = 0.5)
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
                self.ids.tannouncement_card.add_widget(card)

class Tfeedback(Screen):
    def feedback_send(self):
        regex = r'[\s]*'
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
        # x=firebase.get('Users/Student','')
        #for i in x:
        #    if len(txt)<10:
        #        firebase.post('Users/Student/'+i+'/courses/AI/Labs',{'question':txt,'sender':user_info['username'],'time':f"{datetime.now().strftime('%H:%M')}"})
        #    else:
        #        firebase.post('Users/Student/'+i+'/courses/AI/Assignments',{'question':txt,'sender':user_info['username'],'time':f"{datetime.now().strftime('%H:%M')}"})
        if (re.fullmatch(regex, txt)):
            MDDialog(title = "Invalid", text = "Field must not be empty").open()
        else:
            time.sleep(2)
            self.ids.feedback_txt.text = ""
            Snackbar(text="Thanks for your Feedback :)",snackbar_x="10dp",snackbar_y="10dp",size_hint_x=0.5,pos_hint={'center_x': 0.5, 'center_y': 0.1}).open()


class Sfeedback(Screen):
    def feedback_send(self):
        regex = r'[\s]*'
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
        # x=firebase.get('Users/Student','')
        #for i in x:
        #    if len(txt)<10:
        #        firebase.post('Users/Student/'+i+'/courses/AI/Labs',{'question':txt,'sender':user_info['username'],'time':f"{datetime.now().strftime('%H:%M')}"})
        #    else:
        #        firebase.post('Users/Student/'+i+'/courses/AI/Assignments',{'question':txt,'sender':user_info['username'],'time':f"{datetime.now().strftime('%H:%M')}"})
        if (re.fullmatch(regex, txt)):
            MDDialog(title = "Invalid", text = "Field must not be empty").open()
        else:
            time.sleep(2)
            self.ids.feedback_txt.text = ""
            Snackbar(text="Thanks for your Feedback :)",snackbar_x="10dp",snackbar_y="10dp",size_hint_x=0.5,pos_hint={'center_x': 0.5, 'center_y': 0.1}).open()


class Sprofile(Screen):
    loader = None
    def __init__(self, **kwargs):
        super(Sprofile,self).__init__(**kwargs)

    def load(self):
        self.loader = MDDialog(
            size_hint=(None, None),
            size= (0, 0),
            type="custom",
            content_cls=Loader(),
        )
        self.loader.open()

    def attendance(self):
        x = firebase.get("Users/Student/"+user_id+"/courses/",'')
        c=0
        for i in x:
            y = firebase.get("Users/Teacher",'')
            for j in y:
                if (y[j]["course"]["cid"]==i):
                    z=y[j]["day"]
                    l = MDLabel(text=str(i)+" - "+str(round(x[i]["Attendence"]/int(z),1)*100),padding_x=85,font_style="H5",bold=True)
            if (c>=4):
                self.ids.spro_l.add_widget(l)
            else:
                self.ids.spro_r.add_widget(l)
            c=c+1

    def spin(self):
        try:
            self.ids.pro_name.text='Username - ' + user_info["username"]
            self.ids.pro_email.text='Email - ' + user_info["email"]
            self.attendance()
            self.loader.dismiss()
        except:
            pass
    def on_enter(self, *args):
        self.load()
        threading.Thread(target=self.spin).start()

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

class Scourse1(Screen):

    dialog = None
    file_manager = None
    dialog1 = None
    p = ""
    d = None
    loader = None

    def __init__(self, **kw):
        super(Scourse1, self).__init__(**kw)
        # Clock.schedule_interval(self.on_enter,5)

    def joinclass(self):
        webbrowser.open('https://meet.google.com/jpq-webf-iwy?pli=1', new = 1)

    def load(self):
        self.loader = MDDialog(
            size_hint=(None, None),
            size= (0, 0),
            type="custom",
            content_cls=Loader(),
        )
        self.loader.open()

    def lab_title(self):
        self.dialog = MDDialog(
            title="Attention!!!",
            type="custom",
            content_cls=Slab_title(),
            buttons=[
                MDFlatButton(text="CANCEL", on_press = self.cancel),
                MDFlatButton(text="OK", on_press = self.lab_title_ok),
            ],
        )
        self.dialog.open()

    def ass_title(self):
        self.dialog = MDDialog(
            title="Attention!!!",
            type="custom",
            content_cls=Sass_title(),
            buttons=[
                MDFlatButton(text="CANCEL", on_press = self.cancel),
                MDFlatButton(text="OK", on_press = self.ass_title_ok),
            ],
        )
        self.dialog.open()

    def lab_title_ok(self, inst):
        regex = r'[\s]*'
        a = 0
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                t = obj.text

        if(re.fullmatch(regex, t)):
            self.d = MDDialog(title = "Invalid Input", text = "Field must not be empty")
            self.d.open()
            a = 1
        if(a == 0):
            global title
            title = t
            # add something
            self.dialog.dismiss()
            self.uploadlab()

    def ass_title_ok(self, inst):
        regex = r'[\s]*'
        a = 0
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                t = obj.text

        if(re.fullmatch(regex, t)):
            self.d = MDDialog(title = "Invalid Input", text = "Field must not be empty")
            self.d.open()
            a = 1
        if(a == 0):
            global title
            title = t
            # add something
            self.dialog.dismiss()
            self.uploadass()

    def uploadlab(self):
        self.file_manager = MDFileManager(
            select_path = self.select_lp,
            exit_manager = self.exit_manager,
        )
        self.file_manager.show('\\Users\\'+current_user)

    def uploadass(self):
        self.file_manager = MDFileManager(
            select_path = self.select_ap,
            exit_manager = self.exit_manager,
        )
        self.file_manager.show('\\Users\\'+current_user)

    def select_lp(self, path):
        self.p = path
        self.dialog1 = MDDialog(
            title="Confirm ?",
            text = "Are you sure you want to upload this file",
            buttons=[
                MDFlatButton(text="NO", on_press = self.no),
                MDFlatButton(text="YES", on_press = self.lab_load),
            ],
        )
        self.dialog1.open()

    def select_ap(self, path):
        self.p = path
        self.dialog1 = MDDialog(
            title="Confirm ?",
            text = "Are you sure you want to upload this file",
            buttons=[
                MDFlatButton(text="NO", on_press = self.no),
                MDFlatButton(text="YES", on_press = self.ass_load),
            ],
        )
        self.dialog1.open()

    def lab_load(self, inst):
        self.load()
        threading.Thread(target=self.lyes).start()

    def ass_load(self, inst):
        self.load()
        threading.Thread(target=self.ayes).start()

    def lyes(self):
        n = self.p
        n = n.split('\\')

        # Name of the file that should be displayed
        name = n.pop()
        self.dialog1.dismiss()

        # self.p is the path of the file - (LAB file)
        self.p = "C:"+self.p
        storage.child(c1_id+title+name).put(self.p)
        pdf_url=storage.child(c1_id+title+name).get_url(None)
        x = firebase.get("Users/Teacher",'')
        for i in x:
            if (x[i]["username"]==(self.ids.tname.text).replace("Dr. ","")):
                y = x[i]["course"]["Labs"]
                for j in y:
                    if ((y[j]["title"].replace(" ","").lower())==(title.replace(" ","")).lower()):
                        firebase.post("Users/Teacher/"+i+"/course/Labs/"+j+"/student_files/",{"name":user_info["username"],"url":pdf_url})
                        z = firebase.get("Users/Student/"+user_id+"/courses/"+x[i]["course"]["cid"]+"/Labs/",'')
                        for k in z:
                            if ((z[k]["title"].replace(" ","").lower())==(title.replace(" ","")).lower()):
                                firebase.put("Users/Student/"+user_id+"/courses/"+x[i]["course"]["cid"]+"/Labs/"+k+"/","status",1)
                                self.add_labcard()

        self.loader.dismiss()
        self.file_manager.close()
        Snackbar(text="File Successfully uploaded -_- ",snackbar_x="10dp",snackbar_y="10dp",size_hint_x=0.5,pos_hint={'center_x': 0.5, 'center_y': 0.1}).open()

    def ayes(self):
        n = self.p
        n = n.split('\\')

        # Name of the file that should be displayed
        name = n.pop()
        self.dialog1.dismiss()

        # self.p is the path of the file - (Assignment file)
        self.p = "C:"+self.p
        # store the file in firebase
        storage.child(c1_id+title+name).put(self.p)
        pdf_url=storage.child(c1_id+title+name).get_url(None)
        x = firebase.get("Users/Teacher",'')
        for i in x:
            if (x[i]["username"]==(self.ids.tname.text).replace("Dr. ","")):
                y = x[i]["course"]["Assignments"]
                for j in y:
                    if ((y[j]["title"].replace(" ","").lower())==(title.replace(" ","")).lower()):
                        firebase.post("Users/Teacher/"+i+"/course/Assignments/"+j+"/student_files/",{"name":user_info["username"],"url":pdf_url})
                        z = firebase.get("Users/Student/"+user_id+"/courses/"+x[i]["course"]["cid"]+"/Assignments/",'')
                        for k in z:
                            if ((z[k]["title"].replace(" ","").lower())==(title.replace(" ","")).lower()):
                                firebase.put("Users/Student/"+user_id+"/courses/"+x[i]["course"]["cid"]+"/Assignments/"+k+"/","status",1)
                                self.add_asscard()

        self.loader.dismiss()
        self.file_manager.close()
        Snackbar(text="File Successfully uploaded -_- ",snackbar_x="10dp",snackbar_y="10dp",size_hint_x=0.5,pos_hint={'center_x': 0.5, 'center_y': 0.1}).open()

    def exit_manager(self, *args):
        self.file_manager.close()

    def no(self, inst):
        self.dialog1.dismiss()

    def cancel(self, inst):
        self.dialog.dismiss()

    def add_labcard(self):
        # add lab cards
        self.ids.slab.clear_widgets()
        x = firebase.get("Users/Student/"+user_id+"/courses/"+c1_id+"/Labs",'')
        for i in x:
            card = MDCard(orientation='horizontal',size_hint=(None,None),size=(880,100),border_radius=10,radius=[10],elevation=0,padding=10,md_bg_color=[84/255,255/255,103/255,1])
            card_l = MDBoxLayout(orientation='vertical')
            card_l_title = MDLabel(text=x[i]["title"],font_style="H6",bold=True)
            card_l_question = MDLabel(text=x[i]["question"])
            card_r_deadline = MDLabel(text="Deadline : "+x[i]["deadline"],bold=True)

            card_r = MDBoxLayout(orientation='vertical')
            card_l.add_widget(card_l_title)
            card_l.add_widget(card_l_question)
            card.add_widget(card_l)
            card_r.add_widget(card_r_deadline)
            card.add_widget(card_r)
            if (x[i]["status"]==1):
                card_status = MDIconButton(icon="check-circle",user_font_size="36sp",pos_hint={'center_x':0.5 , 'center_y':0.5 })
                card.add_widget(card_status)
            self.ids.slab.add_widget(card)

    def add_asscard(self):
        # add assignment cards
        self.ids.sassignment.clear_widgets()
        x = firebase.get("Users/Student/"+user_id+"/courses/"+c1_id+"/Assignments",'')
        for i in x:
            card = MDCard(orientation='horizontal',size_hint=(None,None),size=(880,100),border_radius=10,radius=[10],elevation=0,padding=10,md_bg_color=[84/255,255/255,103/255,1])
            card_l = MDBoxLayout(orientation='vertical')
            card_l_title = MDLabel(text=x[i]["title"],font_style="H6",bold=True)
            card_l_question = MDLabel(text=x[i]["question"])
            card_r_deadline = MDLabel(text="Deadline : "+x[i]["deadline"],bold=True)

            card_r = MDBoxLayout(orientation='vertical')
            card_l.add_widget(card_l_title)
            card_l.add_widget(card_l_question)
            card.add_widget(card_l)
            card_r.add_widget(card_r_deadline)
            card.add_widget(card_r)
            if (x[i]["status"]==1):
                card_status = MDIconButton(icon="check-circle",user_font_size="36sp",pos_hint={'center_x':0.5 , 'center_y':0.5 })
                card.add_widget(card_status)
            self.ids.sassignment.add_widget(card)

    def open_files(self,link):
        webbrowser.open(link,new=1)

    def add_notescard(self):
        # add notes cards
        self.ids.snotes.clear_widgets()
        x= firebase.get("Courses/"+c1_id,'')
        #c = len(x)
        c = 1
        for i in x:
            card = MDCard(orientation='horizontal',size_hint=(None,None),size=(880,40),border_radius=10,radius=[10],elevation=0,padding=10,md_bg_color=[84/255,255/255,103/255,1],on_release=lambda f:self.open_files(x[i]["url"]))
            card_title = MDLabel(text=str(c)+". "+x[i]["title"],font_style="H5")
            c=c+1
            card.add_widget(card_title)
            self.ids.snotes.add_widget(card)

    def add_info(self):
        tname=""
        temail=""
        day = 1
        x = firebase.get("Users/Teacher",'')
        for i in x:
            if x[i]["course"]["cid"] == c1_id:
                tname = x[i]["username"]
                temail = x[i]["email"]
                day=x[i]["day"]
        self.ids.tname.text = 'Dr. ' + str(tname)
        self.ids.tmail.text = str(temail)

        x = firebase.get("Users/Student/"+user_id+"/courses/"+c1_id,'Attendence')
        self.ids.att_per.text=str(round(int(x)/int(day),1)*100)+" %"

    def on_enter(self, *args):
        self.load()
        threading.Thread(target=self.spin).start()

    def clear(self):
        self.ids.tname.text = ""
        self.ids.tmail.text = ""
        self.ids.att_per.text= ""
        self.ids.snotes.clear_widgets()
        self.ids.sassignment.clear_widgets()
        self.ids.slab.clear_widgets()
    def spin(self):
        try:
            self.add_info()
            self.add_labcard()
            self.add_asscard()
            self.add_notescard()
            self.loader.dismiss()
        except:
            pass

class Tstudentfiles(Screen):
    def __init__(self, **kw):
        super(Tstudentfiles,self).__init__(**kw)
    def clear(self):
        self.ids.std_heading.text=""
        self.ids.std_files.clear_widgets()
    def view(self,link):
        webbrowser.open(link,new=1)
    def on_enter(self, *args):
        self.ids.std_heading.text= str(part_type)+" submission files"
        x = firebase.get("Users/Teacher",'')
        self.ids.std_files.clear_widgets()
        for i in x:
            if (x[i]["course"]["cid"]==user_info["course"]["cid"]):
                y = x[i]["course"][part_type]
                for j in y:
                    z = y[j]["student_files"]
                    for k in z:
                        card = MDCard(orientation='vertical',size_hint=(None,None),size=(870,40),elevation=0,border_radius=10,radius=[0,20,0,20],padding=10,md_bg_color=[12/255,172/255,25/255,1],on_release=lambda f:self.view(z[k]["url"]))
                        card_name = MDLabel(text=z[k]["name"],font_style="H5",halign="center")
                        card.add_widget(card_name)
                        self.ids.std_files.add_widget(card)


class Main(MDApp):
    pass

Main().run()
