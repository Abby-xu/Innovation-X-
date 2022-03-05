from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
import os
import dfgui
from os.path import sep, expanduser, isdir, dirname
import kivy.garden.filebrowser
from kivy import platform
import pandas as pd

class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created
    
    def upload(self):
        sm.current = "upload"


class UploadPopup:
    def __init__(self, homeDir, text='import'):
        self.fbrowser = kivy.garden.filebrowser.FileBrowser(select_string='Select',
                                                            multiselect=True, filters=['*.png'], path=homeDir)
        self.fbrowser.bind(
            on_success=self._fbrowser_success,
            on_canceled=self._fbrowser_canceled,
            on_submit=self._fbrowser_success)
        self.popup = Popup(
            title='select',
            content=self.fbrowser, size_hint=(0.9, 0.9),
            auto_dismiss=False
        )
        self.selected = []

    def start(self):
        self.popup.open()
        return self.selected

    def _fbrowser_success(self, fbInstance):
        if len(fbInstance.selection) == 0:
            return
        for file in fbInstance.selection:
            self.selected.append(os.path.join(fbInstance.path, file))
        print('selected: ' + str(self.selected))
        # for file in self.selected:
        #     xls = pd.read_csv(file)
        # dfgui.show(self.selected)

        self.popup.dismiss()
        self.fbrowser = None

    def _fbrowser_canceled(self, instance):
        self.popup.dismiss()
        self.fbrowser = None


class UploadWindow(Screen):
    img = ObjectProperty(None)
    selected = []

    def file_select(self):
        homeDir = None
        if platform == 'win':
            homeDir = os.environ["HOMEPATH"]
        elif platform == 'android':
            homeDir = os.path.dirname(os.path.abspath(__file__))
        elif platform == 'linux':
            homeDir = os.environ["HOME"]
        self.pop = UploadPopup(homeDir, 'import')
        self.selected = self.pop.start()
        # ProcessWindow.image = self.selected[0]


    

class ProcessWindow(Screen):
    image = ObjectProperty(None)

    


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("main.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), 
CreateAccountWindow(name="create"),
MainWindow(name="main"),
UploadWindow(name="upload"),
ProcessWindow(name="process")]
# ResultWindow(name="result")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
