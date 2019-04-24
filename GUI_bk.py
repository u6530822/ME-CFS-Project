import tkinter as tk
from tkinter import *
import image_to_text
from tkinter import filedialog
from tkinter import font  as tkfont # python 3
import pygubu
from PIL import ImageTk, Image
import check
from tkinter.ttk import *

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

        usnm_lb = tk.Label(self, text="Username")
        usnm_lb.place(x = 120, y = 70)

        self.username_entry = Entry(self, width = 24)
        self.username_entry.place(x = 180, y = 70)

        password_lb = tk.Label(self, text="Password")
        password_lb.place(x = 120, y = 110)

        self.password_entry = Entry(self, show="*", width=24)
        self.password_entry.place(x = 180, y = 110)

        # button1 = tk.Button(self, text="Login", highlightbackground='#3E4149',
        #                     command=lambda: controller.show_frame("PageOne"))

        button_login = tk.Button(self, text="Login", highlightbackground='#3E4149',
                            command = self.check_pswd)
        button_login.place(x = 240, y = 140)

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
        self.openButton.place(x = 230, y = 100)
        # self.frame.pack()
        # img = ImageTk.PhotoImage(Image.open(self.name))
        # panel = Label(root, image = img)
        # panel.pack(side = "bottom", fill = "both", expand = "yes")
        ''' preview of the file
        '''
        self.file_lb = tk.Label(self, text="slected file: ", font=controller.title_font)
        self.file_lb.place(x = 200, y = 150)

        self.fn_entry = StringVar()
        self.file_text = Entry(self, width = 30, textvariable=self.fn_entry)
        self.file_text.place(x = 120, y = 180)

        ''' Submit button - To start conversion
        '''
        button = tk.Button(self, text="Start conversion", highlightbackground='#3E4149',
                           command=lambda: self.callback(self.name))
        button.place(x = 190, y = 230)

    def callback(self, name):
        self.controller.show_frame("PageTwo")
        print("printing " + name + " please wait")
        object2 = image_to_text.ImageToText(name)
        object2.print_filename()
        print("done printing " + name)
        self.result = object2

    def open_file(self):
        """Open file."""
        self.master.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes=(("png files","*.png"),("all files","*.*")))
        print(self.master.filename)
        self.name = self.master.filename
        print("open file" + self.name)
        self.fn_entry.set(self.name)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Result page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.createTable()
        self.insert_values()

        edit_button = tk.Button(self, text = "Edit Values", highlightbackground='#3E4149')
        edit_button.pack(pady = 20)
        
        submit_to_dbs_button = tk.Button(self, text="Submit to DBS", highlightbackground='#3E4149',
                           command=lambda: controller.show_frame("StartPage"))
        # do nothing here
        submit_to_dbs_button.pack()


    def createTable(self):
        tv = Treeview(self)
        tv['columns'] = ('values', 'content')
        tv.heading("#0", text='Attributes', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('values', text='Values')
        tv.column('values', anchor='center', width=100)
        tv.heading('content', text='Content')
        tv.column('content', anchor='center', width=100)
        tv.grid(sticky = (N,S,W,E))
        self.treeview = tv
        self.treeview.pack(pady = 20)

# colors = ['red', 'green', 'orange', 'white', 'yellow', 'blue']

# r = 0
# for c in colors:
#     Label(text=c, relief=RIDGE,  width=25).grid(row=r, column=0)
#     Entry(bg=c,   relief=SUNKEN, width=50).grid(row=r, column=1)
#     r = r+1

    def insert_values(self):
        self.treeview.insert('', 'end', text="Sodium", values=("138",
                             '-'))
        self.treeview.insert('', 'end', text="Potassium", values=("5.4",
                             'high'))
        self.treeview.insert('', 'end', text="Chloride", values=("103",
                             '-'))
        self.treeview.insert('', 'end', text="Bicarbonate", values=("30",
                             '-'))
        self.treeview.insert('', 'end', text="Creatinine", values=("92",
                             '-'))
        self.treeview.insert('', 'end', text="eGFR", values=("82",
                             '-'))
        self.treeview.insert('', 'end', text="T.Protein", values=("77",
                             '-'))
        self.treeview.insert('', 'end', text="Albumin", values=("47",
                             '-'))
        self.treeview.insert('', 'end', text="ALP", values=("76",
                             '-'))
        self.treeview.insert('', 'end', text="Bilirubin", values=("12",
                             '-'))
        self.treeview.insert('', 'end', text="GGT", values=("49",
                             '-'))
        self.treeview.insert('', 'end', text="AST", values=("39",
                             '-'))
        self.treeview.insert('', 'end', text="ALT", values=("52",
                             'high'))
        self.treeview.insert('', 'end', text="Other", values=("-",
                             '-'))



    def insert_results(string):
        print("In the loop")
        TextArea = Text()
        TextArea.pack(expand=YES, fill=BOTH)
        '''result is the result string
        '''
        TextArea.insert('1.0',string)
