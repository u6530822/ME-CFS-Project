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

        self.k = tk.Label(text="Username")
        self.k.place(x=140, y=80)
        self.username = Text(self, height=1, width=10)
        self.username.place(x=200, y=80)
        self.w = tk.Label(text="Password")
        self.w.place(x=140, y=100)
        self.password = Text(self, height=1, width=10)
        self.password.place(x=200, y=100)

# e1 = Entry(master, width = 100)
# e1.grid(row=0, column=1, columnspan=30)

#  if pswd matches,show frame
        self.button1 = tk.Button(self, text="Login", highlightbackground='#3E4149',
                            command=lambda :StartPage.first_button_response(self) ,).place(x=220,y=140)
#        self.button1.grid_location(x=100,y=400)
#        self.button1.pack()

    def first_button_response(self):
        '''Checks and calls the reset function for the fields or moves to next page'''
#        self.button1.pack_forget()
        username_input = self.username.get('1.0', 'end-1c') #Getting input from the textfield
        password_input = self.password.get('1.0', 'end-1c')

        if username_input != "mecfs" and password_input != "mecfs": #accepted username and password
            StartPage.login_security(self)

        self.k.destroy() #Removes the label username
        self.w.destroy() #Removes the label password
        self.controller.show_frame("PageOne")

    def login_security(self):
        '''Checks resets the fields if password and username don't match'''
        print("reached here")
        self.username.delete('1.0',END)
        self.password.delete('1.0',END)
        self.mainloop()

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
