import tkinter as tk
from tkinter import *
import image_to_text
from tkinter import filedialog
from tkinter import font  as tkfont  # python 3
from PIL import ImageTk, Image
import check
from tkinter.ttk import *
import boto3
import DBAccessKey
from boto3.dynamodb.conditions import Key, Attr

access_key_id_global=DBAccessKey.DBAccessKey.access_key_id_global
secret_access_key_global=DBAccessKey.DBAccessKey.secret_access_key_global



class GUI:
    name = ""
    frames = {} #Nigel - Change this to global so that new frames can be added to it on the fly
    filtered_output = [] #Nigel - Global variable to store filtered values

    def __init__(self):
        # tk.Tk.__init__(self, *args, **kwargs)

        self.master = Tk()
        self.master.minsize(500, 500)
        # self.frame = tk.Frame(self.master)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self.master)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        global frames #Nigel - Change this to global so that new frames can be added to it on the fly
        frames = {} #Nigel - Change this to global so that new frames can be added to it on the fly

        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
            # frame.pack()

        self.show_frame("PageTwo")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to ME/CFS", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        usnm_lb = tk.Label(self, text="Username")
        usnm_lb.place(x=120, y=70)

        self.username_entry = Entry(self, width=24)
        self.username_entry.place(x=180, y=70)

        password_lb = tk.Label(self, text="Password")
        password_lb.place(x=120, y=110)

        self.password_entry = Entry(self, show="*", width=24)
        self.password_entry.place(x=180, y=110)

        # button1 = tk.Button(self, text="Login", highlightbackground='#3E4149',
        #                     command=lambda: controller.show_frame("PageOne"))

        button_login = tk.Button(self, text="Login", highlightbackground='#3E4149',
                                 command=self.check_pswd)
        button_login.place(x=240, y=140)

    def check_pswd(self):
        username_tocheck = self.username_entry.get()
        password_tocheck = self.password_entry.get()
        login_checker = check.LoginCheck(username_tocheck, password_tocheck)
        # print(login_checker.check_login())
        if (login_checker.check_login()):
            self.controller.show_frame("PageTwo")
        else:
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        label = tk.Label(self, text="Image Upload", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.name = ()

        ''' Open button - To select file
        '''
        self.openButton = tk.Button(self, text='Open', highlightbackground='#3E4149', command=self.open_file)
        self.openButton.place(x=180, y=140)
        # self.frame.pack()
        # img = ImageTk.PhotoImage(Image.open(self.name))
        # panel = Label(root, image = img)
        # panel.pack(side = "bottom", fill = "both", expand = "yes")
        ''' preview of the file
        '''
      #  self.file_lb = tk.Label(self, text="selected file: ", font=controller.title_font)
      #  self.file_lb.place(x=180, y=150)

        self.fn_entry = StringVar()
        self.file_text = Entry(self, width=30, textvariable=self.fn_entry)
        self.file_text.place(x=160, y=110)

        ''' Submit button - To start conversion
        '''
        button = tk.Button(self, text="Start Conversion", highlightbackground='#3E4149',
                           command=lambda: self.callback(self.name))
        button.place(x=230, y=140)

        ''' Filter function
        '''
        #Box to enter Ref no
        self.filter_entry = StringVar()
        self.filter_text = Entry(self, width=30, textvariable=self.filter_entry)
        self.filter_text.place(x=160, y=200)

        #Button to execute
        button = tk.Button(self, text="Filter", highlightbackground='#3E4149',
                           command=lambda: self.get_DB(self.filter_entry.get()))

        button.place(x=230, y=230)


    def callback(self, name):
        self.controller.show_frame("PageTwo")
        print("printing " , name , " please wait")
        object2 = image_to_text.ImageToText(name)
        object2.print_filename()
        print("done printing ", name)
        self.result = object2
        # self.result_files = image_to_text.list_of_dict

    def open_file(self):

        """Open file.
        /Users/Julius/Downloads/ME/ME-CFS-Project/Sample.png
        """
        self.master.filename = filedialog.askopenfilenames(initialdir="/", title="Select file",
                                                          filetypes=(("png files", "*.png"), ("all files", "*.*")))
        print(self.master.filename)
        self.name = self.master.filename
        print("open file", self.name)
        self.fn_entry.set(self.name)

    ##function for filter after button is pressed - Created by Nigel
    def get_DB(self, Ref_no):

        print("Ref no is "+Ref_no)

        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id=access_key_id_global,
                                  aws_secret_access_key=secret_access_key_global)
        table = dynamodb.Table('ME_CFS_DB')

        response = table.query(
            KeyConditionExpression=Key('Reference_No').eq(Ref_no)
        )

        if response['Items']:
            print("start of filter")
            for i in response['Items']:
                if i['Reference_No'] == Ref_no:
                    for key in i.keys():
                        perline = key + ": " + str(i[key])
                        GUI.filtered_output.append(perline)
        else:
            print("Not found")
            GUI.filtered_output.append("Not found")

        frame = FilterPage(parent=self.parent, controller=self.controller)
        frames[FilterPage.__name__] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        GUI.show_frame(self.controller, "FilterPage")

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Result page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
# get list from img2txt here
        self.result_files = [{'filename': 'file1', 'Sodium': '138', 'Potassium': '5.4'},
                                {'filename': 'file2', 'Sodium': '138', 'Potassium': '5.4'}]
                                
        print("List of Dict in page 2: ",image_to_text.list_of_dict)
        #self.result_files = image_to_text.list_of_dict
        self.file_lstbx = Listbox(self)
        self.file_lstbx.bind('<<ListboxSelect>>', self.display_selected_file)
        for file_name in self.result_files:
            self.file_lstbx.insert(END, file_name["filename"])
        self.file_lstbx.pack()
        # TODO: change x and y position

        self.createTable()
        # self.insert_values()


        submit_to_dbs_button = tk.Button(self, text="Submit to DBS", highlightbackground='#3E4149',
                                         command = self.DBS_upload())

        submit_to_dbs_button.pack()

    def DBS_upload(self):
    	# Young 
    	# self.resultfiles
    	# for items in list
    	# imgtotext.update_DB
    	print("in DBS_upload")

    def display_selected_file(self, event):
        idx=(self.file_lstbx.curselection()[0])
        # self.result_files = image_to_text.list_of_dict
        display_dict = self.result_files[idx]
        self.treeview.delete(*self.treeview.get_children())
        self.insert_values(display_dict)


    def createTable(self):
        tv = Treeview(self)
        tv['columns'] = ('values')
        tv.heading("#0", text='Attributes', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('values', text='Values')
        tv.column('values', anchor='center', width=50)
        # tv.heading('content', text='Content')
        # tv.column('content', anchor='center', width=50)
        tv.bind('<Double-1>', self.onDoubleClick) # Double-click the left button to enter the edit

        vsb = tk.Scrollbar(tv, orient="vertical", command=tv.yview)
        vsb.place(x=387, y=0, height=230)
        tv.configure(yscrollcommand=vsb.set)
        # TODO: figure out where to place the scroll bar

        #tv.grid(sticky=(N, S, W, E))   # not sure why this line gives me error
        self.treeview = tv
        self.treeview.pack(pady=5)

    def onDoubleClick(self, event):
        ''' Executed, when a row is double-clicked. Opens 
        read-only EntryPopup above the item's column, so it is possible
        to select text '''
        item = self.treeview.selection()[0] # now you got the item on that tree
        print ("you clicked on " + item)

        # close previous popups
        # self.destroyPopups()

        # what row and column was clicked on
        rowid = self.treeview.identify_row(event.y)
        columnid = self.treeview.identify_column(event.x)

        # TODO: change the position of entry and ok button
        cn = int(str(columnid).replace('#',''))
        rn = int(str(rowid).replace('I',''))

        entryedit = Text(self.treeview, width=10+(cn-1)*16,height = 1)
        entryedit.place(x=200, y=6+rn*20)

        def saveedit():
            changed_value = entryedit.get(0.0, "end").rstrip("\n")
            attri_text = self.treeview.item(self.treeview.focus())["text"]
            self.treeview.set(item, column = columnid, value = changed_value)
            dict_to_change = {
                attri_text : changed_value
            }
            self.result_dict.update(dict_to_change)
            # update array
            print(self.result_dict)
            entryedit.destroy()
            confirm_button.destroy()
            # TODO: change x y position here
        confirm_button = tk.Button(self, text='OK', width=4, command=saveedit)
        confirm_button.place(x=455+(cn-1)*242,y=240+rn*20)
        
    def insert_values(self, display_dict):
        # self.result_dict = {'filename': 'filename', 'Sodium': '138', 'Potassium': '5.4', 'Chloride': '103', 'Bicarbonate': '30', 'Urea': '4.8', 'Creatinine': '92', 'eGFR': '82', 'Albumin': '47', 'ALP': '76', 'Bilirubin': '12', 'GGT': '49', 'AST': '39', 'ALT': '52'}
        self.result_dict = display_dict
        # print(self.result_dict)
        for result in self.result_dict.items():
            self.treeview.insert('', 'end', text=result[0], values=(result[1]))

#Created by Nigel
class FilterPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Filtered Result", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        print(GUI.filtered_output)

        #self.filter_entry = StringVar()
        #self.filter_text = Label(self, textvariable=self.filter_entry, relief=RAISED)
        #self.filter_entry.set(GUI.filtered_output)
        #self.filter_text.place(x=160, y=50)

        print("end of filter")


        self.createTable()
        # self.insert_values()

    def createTable(self):
        tv = Treeview(self, height=20)
        tv['columns'] = ('values')
        tv.heading("#0", text='Attributes', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('values', text='Values')
        tv.column('values', anchor='center', width=50)
        vsb = tk.Scrollbar(tv, orient="vertical", command=tv.yview)
        vsb.place(x=387, y=0, height=30)
        tv.configure(yscrollcommand=vsb.set)
        # TODO: figure out where to place the scroll bar

        self.treeview = tv
        self.treeview.pack(pady=5)

        self.insert_values(GUI.filtered_output)

    def insert_values(self, display_dict):
        self.result_dict = display_dict
        for result in self.result_dict:
            result2 = result.split(": ")
            print("result is " + result)
            self.treeview.insert('', 'end', text=result2[0], values=(result2[1]))