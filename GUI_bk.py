import tkinter as tk
from tkinter import *
import image_to_text
from tkinter import filedialog
from tkinter import font  as tkfont # python 3
#import pygubu


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

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to ME/CFS\n input username and pswd", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        username = Text(self, height = 2, width = 10)
        username.pack(expand=YES, fill=BOTH)

        password = Text(self, height = 2, width = 10)
        password.pack(expand=YES, fill=BOTH)

#        widget = Entry(parent, show="*", width=15)
#        widget.pack()

#  if pswd matches,show frame
        button1 = tk.Button(self, text="Login",
                            command=lambda: controller.show_frame("PageOne"))
        button1.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="open filedialog", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.name = ""

        ''' Open button - To select file
        '''
        self.openButton = tk.Button(self, text='open', command=self.open_file)
        self.openButton.pack()
        # self.frame.pack()


        # ''' Submit button - To start conversion
        # '''
        # self.button_confirm = Button(self.master, text="SUBMIT", command=lambda: self.callback(self.name))
        # self.button_confirm.pack()
        # self.frame.pack()

        #button = tk.Button(self, text="Submit",
        #                   command=lambda: controller.show_frame("PageTwo"))
        button = tk.Button(self, text="Submit",
                           command=lambda: self.callback(self.name))

        self.button_confirm = Button(self.master, text="SUBMIT", command=lambda: self.callback(self.name))

        button.pack()

    def callback(self, name):
        print("click!")
        print("printing " + name + " please wait")
        object2 = image_to_text.ImageToText(name)
        object2.print_filename()
        print("done printing " + name)

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

        button = tk.Button(self, text="Submit to DBS",
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


