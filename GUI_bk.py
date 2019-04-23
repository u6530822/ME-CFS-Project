import tkinter as tk
from tkinter import *
import image_to_text
from tkinter import filedialog
from tkinter import font  as tkfont # python 3
import pygubu
from PIL import ImageTk, Image
import check

class GUI:

    name = ""

    def __init__(self):
        # tk.Tk.__init__(self, *args, **kwargs)

        self.master = Tk()
        self.master.minsize(500,500)
        # self.frame = tk.Frame(self.master)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self.master)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
            # frame.pack()

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to ME/CFS", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        usnm_lb = tk.Label(self, text="username", font=controller.title_font)
        usnm_lb.place(x = 140, y = 70)

        self.username_entry = Entry(self, width = 24)
        self.username_entry.place(x = 140, y = 100)

        password_lb = tk.Label(self, text="password", font=controller.title_font)
        password_lb.place(x = 140, y = 130)

        self.password_entry = Entry(self, show="*", width=24)
        self.password_entry.place(x = 140, y = 160)

        # button1 = tk.Button(self, text="Login", highlightbackground='#3E4149',
        #                     command=lambda: controller.show_frame("PageOne"))

        button_login = tk.Button(self, text="Login", highlightbackground='#3E4149',
                            command = self.check_pswd)
        button_login.place(x = 220, y = 200)

    def check_pswd(self):
        username_tocheck = self.username_entry.get()
        password_tocheck = self.password_entry.get()
        login_checker = check.LoginCheck(username_tocheck, password_tocheck)
        # print(login_checker.check_login())
        if (login_checker.check_login()):
            self.controller.show_frame("PageOne")
        else:
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Image Upload", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.name = ""

        ''' Open button - To select file
        '''
        self.openButton = tk.Button(self, text='open', highlightbackground='#3E4149', command=self.open_file)
        self.openButton.pack()
        # self.frame.pack()
        # img = ImageTk.PhotoImage(Image.open(self.name))
        # panel = Label(root, image = img)
        # panel.pack(side = "bottom", fill = "both", expand = "yes")


        ''' Submit button - To start conversion
        '''
        # self.button_confirm = Button(self.master, text="SUBMIT", command=lambda: self.callback(self.name))
        # self.button_confirm.pack()
        # self.frame.pack()
        button = tk.Button(self, text="Submit", highlightbackground='#3E4149',
                           command=lambda: self.callback(self.name))
        button.pack()

    def callback(self, name):
        print("click!")
        print("printing " + name + " please wait")
        object2 = image_to_text.ImageToText(name)
        object2.print_filename()
        print("done printing " + name)
        self.result = object2
        self.controller.show_frame("PageTwo")

    def open_file(self):
        """Open file."""
        self.master.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes=(("png files","*.png"),("all files","*.*")))
        print(self.master.filename)
        self.name = self.master.filename
        print("open file" + self.name)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Result page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

       # TextArea = Text()
       # TextArea.pack(expand=YES, fill=BOTH)
        '''result is the result string
        '''
        # TextArea.insert(result)

        button = tk.Button(self, text="Submit to DBS", highlightbackground='#3E4149',
                           command=lambda: controller.show_frame("StartPage"))
        # do nothing here
        button.pack()

    def insert_results(string):
        print("In the loop")
        TextArea = Text()
        TextArea.pack(expand=YES, fill=BOTH)
        '''result is the result string
        '''
        TextArea.insert('1.0',string)
