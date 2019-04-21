from tkinter import filedialog
import tkinter as tk
from tkinter import *
import image_to_text


class GUI:

    def __init__(self):
        ''' Init settings
        '''
        self.master = Tk()
        self.frame = tk.Frame(self.master)

        self.master.minsize(1080, 720)
        # self.master.geometry("320x100")
        self.master.title('ME/FCS')

        ''' Label username
        '''
        lab_var = StringVar()
        label = Label(self.master, textvariable=lab_var, relief=RAISED)
        lab_var.set("username")
        # label.place(x=20, y=60)
        # label.pack()
        label.pack(padx=50, pady=10)

        ''' textBox username
        '''
        var = StringVar()
        textbox_username = Entry(self.master, textvariable=var)
        # textbox.focus_set()
        # textbox.config(width = 5)
        # textbox.pack(pady=150, padx=150)
        # textbox.pack(ipadx=150, ipady=150)
        # textbox_username.pack(ipadx=5, ipady=2)
        textbox_username.pack()

        ''' Label pswd
        '''
        lab_var = StringVar()
        lab_pswd = Label(self.master, textvariable=lab_var, relief=RAISED)
        lab_var.set("password")
        lab_pswd.pack(padx=50, pady=10)

        ''' textBox pswd
        '''
        var = StringVar()
        textbox_pswd = Entry(self.master, textvariable=var)
        textbox_pswd.pack(pady=10)

        ''' Login Button
        '''
        self.button_login = tk.Button(self.frame, text='Login', width=25, command=self.open_upload)
        self.button_login.pack()
        self.frame.pack()

    def open_upload(self):
        # TODO : check password and username
        self.newWindow = tk.Toplevel(self.master)
        self.app = Upload(self.newWindow)


class Upload:
    # TODO: remove references between both windows to destroy the login window without destroying the upload window
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.minsize(1080, 720)

        ''' TODO: Label Drop File
        '''
        drop_str = StringVar()
        drop_lb = Label(self.master, textvariable=drop_str, relief=RAISED)
        drop_str.set("drop file")
        drop_lb.pack(ipadx=50, ipady=50)

        ''' TODO: textBox to edit
        '''
        var = StringVar()
        textbox_username = Entry(self.master, textvariable=var)
        textbox_username.pack(ipadx=50, ipady=50)

        self.name = ""

        ''' Open button - To select file
        '''
        self.openButton = tk.Button(self.frame, text='open', command=self.open_file)
        self.openButton.pack()
        self.frame.pack()

        ''' Submit button - To start conversion
        '''
        self.button_confirm = Button(self.master, text="SUBMIT", command=lambda: self.callback(self.name))
        self.button_confirm.pack()
        self.frame.pack()

# functions

    def open_file(self):
        """Open file."""
        self.master.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes=(("png files","*.png"),("all files","*.*")))
        print(self.master.filename)
        self.name = self.master.filename
        print("open file" + self.name)

    def callback(self, name):
        """Convert image to text."""
        print("click!")
        print("printing " + name + " please wait")
        object2 = image_to_text.ImageToText(name)
        object2.print_filename()
        print("done printing " + name)

    '''
    def open_results(self):
        # TODO: Do we need this?
        self.newWindow = tk.Toplevel(self.master)
        self.app = Result(self.newWindow)

    def donothing(self):
        x = 0

    def close_windows(self):
        self.master.destroy()
    '''


# TODO: Display result on textbox
class Result:

    def __init__(self, master):
        ''' result text
        '''
        result = StringVar()
        textbox = Entry(self.master, textvariable=result)
        textbox.focus_set()
        textbox.config(width=500)
        textbox.pack(pady=100, padx=100)

        # frame=Frame(self.master, width=300, height=600)
        # frame.pack()
        # TextArea = Text()
        # TextArea.pack(expand=YES, fill=BOTH)

        # textbox.place(x=100, y=100, width = 500, height = 600)

        # tbox1 = Text(frame)
        # tbox1.place(x=10, y=115, height=30, width=200)




