from tkinter import filedialog
from tkinter import *
import image_to_text


class GUI:
    name = ""

    def __init__(self):
        self.master = Tk()

        ''' Basic settings
        '''
        self.master.minsize(300,100)
        self.master.geometry("320x100")
        self.master.title('ME/FCS')
        Label(self.master, text='test').pack(pady=20,padx=50)

        ''' textfield
        '''
        var = StringVar()
        textbox = Entry(self.master, textvariable=var)
        textbox.focus_set()
        textbox.pack(pady=10, padx=10)

        ''' img
        '''
        # img = PhotoImage(file="logo2.png")
        # panel = Label(master, image = img)
        # panel.pack(side = "bottom", fill = "both", expand = "yes")

        ''' open file
        '''
        self.master.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
        print(self.master.filename)
        name = self.master.filename

        ''' BUTTON 
                SUBMIT
        '''
        button = Button(self.master, text = "SUBMIT", command = lambda: self.callback(name))
        button.pack()
        button.place(x = 200, y = 50)

        ''' MENUBAR 
                file - new open save | exit
                help - help index search, about
        '''
        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=menubar)

    ''' functions
    '''
    def callback(self, name):
        print("click!")
        print("printing " + name + " please wait")
        object2 = image_to_text.ImageToText(name)
        object2.print_filename()
        print("done printing " + name)

    def donothing(self):
        x = 0

