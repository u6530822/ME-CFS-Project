from Tkinter import *
import os
import Tkinter, Tkconstants, tkFileDialog

master = Tk()
''' Basic settings
'''
master.minsize(300,100)
master.geometry("320x100")
master.title('ME/FCS')
Label(master, text='test').pack(pady=20,padx=50)

''' textfield
'''
var = StringVar()
textbox = Entry(master, textvariable=var)
textbox.focus_set()
textbox.pack(pady=10, padx=10)

''' img
'''
# img = PhotoImage(file="logo2.png")
# panel = Label(master, image = img)
# panel.pack(side = "bottom", fill = "both", expand = "yes")

''' functions
'''
def callback():
	print "click!"
def donothing():
   x = 0

''' open file
'''
master.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
print (master.filename)

''' BUTTON 
		SUBMIT
'''
button = Button(master, text = "SUBMIT", command = callback)
button.pack()
button.place(x = 200, y = 50)

''' MENUBAR 
		file - new open save | exit
		help - help index search, about
'''
menubar = Menu(master)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=master.quit)
menubar.add_cascade(label="File", menu=filemenu)
 
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)
 
master.config(menu=menubar)


master.mainloop()