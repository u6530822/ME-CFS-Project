import tkinter as tk
from tkinter import *
import image_to_text
from tkinter import filedialog
from tkinter import font  as tkfont  # python 3
from PIL import ImageTk, Image
import check
# from tkinter import ttk
from tkinter.ttk import *
import boto3
import DBAccessKey
from boto3.dynamodb.conditions import Key, Attr

access_key_id_global = DBAccessKey.DBAccessKey.access_key_id_global
secret_access_key_global = DBAccessKey.DBAccessKey.secret_access_key_global


class GUI:
    name = ""
    frames = {}  # Nigel - Change this to global so that new frames can be added to it on the fly
    filtered_output = []  # Nigel - Global variable to store filtered values

    def __init__(self):
        # tk.Tk.__init__(self, *args, **kwargs)

        self.master = Tk()
        self.master.minsize(500, 500)
        self.master.title("ME CFS")
        # self.frame = tk.Frame(self.master)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

        container = tk.Frame(self.master)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # self.image = Image.open("bgimg.gif")
        # self.img_copy = self.image.copy()
        #
        # self.background_image = ImageTk.PhotoImage(self.image)
        #
        # self.background = Label(self.master, image=self.background_image)
        # self.background.pack(fill=BOTH, expand=YES)

        global frames
        frames = {}
        # Nigel - Change this to global so that new frames can be added to it on the fly

        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
            # frame.place(x = 0, y = 0)

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.image = Image.open("bgimg.gif")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.place(x=0, y=0)

        # style = tk.ttk.Style()
        # style.configure("BW.TLabel", foreground="black", background="white")
        # l1 = ttk.Label(text="Test", style="BW.TLabel")
        # l1.place(x=0, y=0)
        # TODO change label bg using ttk or canvas

        label = tk.Label(self, text="Welcome to ME/CFS", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        usnm_lb = tk.Label(self, text="Username")
        usnm_lb.place(x=120, y=70)

        self.username_entry = Entry(self, width=24)
        self.configure(highlightthickness=0, highlightbackground="black", borderwidth=0)
        self.username_entry.place(x=180, y=70)
        password_lb = tk.Label(self, text="Password")
        password_lb.place(x=120, y=110)

        self.password_entry = Entry(self, show="*", width=24)
        self.password_entry.place(x=180, y=110)

        # button1 = tk.Button(self, text="Login", highlightbackground='#3E4149',
        #                     command=lambda: controller.show_frame("PageOne"))

        button_login = tk.Button(self, text="Login", highlightbackground='#3E4149',
                                 command=self.check_pswd)
        button_login.place(x=230, y=140)

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

        self.image = Image.open("bgimg.gif")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.place(x=0, y=0)

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
        # Box to enter Ref no
        self.filter_entry = StringVar()
        self.filter_text = Entry(self, width=30, textvariable=self.filter_entry)
        self.filter_text.place(x=160, y=200)

        # Button to execute
        button = tk.Button(self, text="Filter", highlightbackground='#3E4149',
                           command=lambda: self.get_DB(self.filter_entry.get()))

        button.place(x=230, y=230)

    def callback(self, name):
        self.controller.show_frame("PageTwo")
        print("printing ", name, " please wait")
        object_img2txt = image_to_text.ImageToText(name)
        object_img2txt.print_filename()
        print("done printing ", name)
        # self.result = object2
        # self.result_files = image_to_text.list_of_dict

    def open_file(self):
        self.master.filename = filedialog.askopenfilenames(initialdir="/", title="Select file",
                                                           filetypes=(("png files", "*.png"), ("all files", "*.*")))
        print(self.master.filename)
        self.name = self.master.filename
        print("open file", self.name)
        self.fn_entry.set(self.name)

    #function for filter after button is pressed - Created by Nigel
    def get_DB(self, Ref_no):

        print("Ref no is " + Ref_no)

        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id=access_key_id_global,
                                  aws_secret_access_key=secret_access_key_global)
        table = dynamodb.Table('ME_CFS_DB')

        response = table.query(
            KeyConditionExpression=Key('Reference_No').eq(Ref_no)
        )

        if response['Items']:
            for i in response['Items']:
                if i['Reference_No'] == Ref_no:
                    for key in i.keys():
                        perline = key + ": " + str(i[key])
                        GUI.filtered_output.append(perline)
            print("start of filter")
            frame = FilterPage(parent=self.parent, controller=self.controller)
            frames[FilterPage.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            GUI.show_frame(self.controller, "FilterPage")
        else:
            print("Not found")
            # self.filter_entry(0, 'end')
            self.filter_entry.set("Invalid Reference No.")
            # GUI.filtered_output.append("Not found")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.image = Image.open("bgimg.gif")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.place(x=0, y=0)

        label = tk.Label(self, text="Result page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.result_files = [{'filename': 'Sample1', 'Sodium': '138', 'Potassium': '5.4'}]
        self.result_dict = image_to_text.list_of_dict
        self.file_lstbx = Listbox(self)
        self.file_lstbx.bind('<B1-Motion>', self.insert_files)
        # TODO: click once or the page is viewed
        self.file_lstbx.bind('<<ListboxSelect>>', self.display_selected_file)
        self.file_lstbx.pack()
        # testvis = self.master.wait_visibility() # run event loop until window appearss
        # self.master.wait_variable(self.result_files)
        # self.master.after_idle(self.insert_files)
        self.createTable()
        # self.create_entry_table()
        submit_to_dbs_button = tk.Button(self, text="Upload", highlightbackground='#3E4149',
                                         command=lambda: self.DBS_upload())
        submit_to_dbs_button.pack()
        back_previous_bt = tk.Button(self, text="Back", highlightbackground='#3E4149',
                                     command=self.back_previous_page)
        # command=lambda: self.controller.show_frame("PageOne"))
        # TODO: clear the self.file_dict, img2txt list clear, call clear_content()

        back_previous_bt.place(x=0, y=0)

    def insert_values(self, display_dict):
        self.treeview.delete(*self.treeview.get_children())
        # def insert_values(self, display_dict):
        self.treeview.destroy()
        self.createTable()
        self.result_dict = display_dict
        for result in self.result_dict.items():
            id = self.treeview.insert('', 'end', text=result[0], values=(result[1]))
            # print(id)

    def onDoubleClick(self, event):
        ''' Executed, when a row is double-clicked. Opens
        read-only EntryPopup above the item's column, so it is possible
        to select text '''
        # TODO: only allow create one entry

        item = self.treeview.selection()[0]  # now you got the item on that tree
        event_value = self.treeview.item(self.treeview.focus())["values"][0]
        curr_tree_item = self.treeview.item(self.treeview.focus())
        # print(curr_tree_item)
        # what row and column was clicked on
        rowid = self.treeview.identify_row(event.y)
        # TODO rowid correction with HEX
        columnid = self.treeview.identify_column(event.x)
        rn = int(str(rowid).replace('I', ''))
        cn = int(str(columnid).replace('#', ''))
        # print("rowid = ", rowid, "rn = ", rn)

        # TODO: calculate scrolled position
        entryedit = Text(self.treeview, width=10 + (cn - 1) * 16, height=1)
        entryedit.insert(END, event_value)
        # TODO: insert initial value at init
        entryedit.place(x=200, y=6 + rn * 20)

        def saveedit():
            changed_value = entryedit.get(0.0, "end").rstrip("\n")
            attri_text = self.treeview.item(self.treeview.focus())["text"]
            self.treeview.set(item, column=columnid, value=changed_value)
            dict_to_change = {
                attri_text: changed_value
            }
            self.result_dict.update(dict_to_change)
            # print(self.result_dict)
            entryedit.destroy()
            confirm_button.destroy()

        confirm_button = tk.Button(self, text='OK', width=4, command=saveedit)
        confirm_button.place(x=455 + (cn - 1) * 242, y=240 + rn * 20)

    def DBS_upload(self):
        print("in DBS_upload:", self.result_dict)
        string_val = self.result_dict['Reference_No']
        print("String val:", string_val)
        boolean_val = image_to_text.ImageToText.check_entry_exist(string_val)
        print("if that entry already exist:", boolean_val)
        if (boolean_val):
            print("Update it")
            # update it only
            for val in self.result_dict:
                if (val != 'Reference_No' and val != 'Date_Time'):
                    print("Resuld_dict:", val, " value:", self.result_dict[val])
                    val1 = val.replace('.', '_')
                    image_to_text.ImageToText.update_DB(val1, self.result_dict[val], self.result_dict['Reference_No'],
                                                        self.result_dict['Date_Time'])

        else:
            print("Create it")
            # create it and update it
            image_to_text.ImageToText.write_to_DB(self.result_dict['Reference_No'], self.result_dict['Date_Time'])
            for val in self.result_dict:
                if (val != 'Reference_No' and val != 'Date_Time'):
                    print("Resuld_dict:", val, " value:", self.result_dict[val])
                    val1 = val.replace('.', '_')
                    image_to_text.ImageToText.update_DB(val1, self.result_dict[val], self.result_dict['Reference_No'],
                                                        self.result_dict['Date_Time'])

    def insert_files(self, event):
        # print("MOVE")
        self.file_lstbx.delete(0, END)
        self.result_files = image_to_text.list_of_dict
        # test_result_files
        '''
        self.result_files = [{'filename': 'Sample1', 'Sodium': '138', 'Potassium': '5.4'},
                             {'filename': 'Sample2', 'Sodium': '138', 'Potassium': '5.4'},
                             {'filename': 'Sample3', 'Sodium': '138', 'Potassium': '5.4'},
                             {'filename': 'Sample4', 'Sodium': '138', 'Potassium': '5.4'}]
                             '''

        for file_name in self.result_files:
            short_filename = file_name["filename"].split('/')
            # print("filename:", short_filename)
            filename_display = short_filename[-1]
            self.file_lstbx.insert(END, filename_display)
            # self.file_lstbx.insert(END, file_name["filename"])

    def display_selected_file(self, event):
        # self.file_lstbx.delete(0, END)
        idx = (self.file_lstbx.curselection()[0])
        display_dict = self.result_files[idx]
        self.treeview.delete(*self.treeview.get_children())
        self.insert_values(display_dict)

    def createTable(self):
        tv = Treeview(self)
        tv['columns'] = ('values', 'comment')
        tv.heading("#0", text='Attributes', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('values', text='Values')
        tv.column('values', anchor='center', width=80)
        tv.heading('comment', text='Comment')
        tv.column('comment', anchor='center', width=80)
        tv.bind('<Double-1>', self.onDoubleClick)  # Double-click the left button to enter the edit

        vsb = tk.Scrollbar(tv, orient="vertical", command=tv.yview)
        vsb.place(x=387, y=0, height=230)
        tv.configure(yscrollcommand=vsb.set)
        # TODO: figure out where to place the scroll bar

        # tv.grid(sticky=(N, S, W, E))   # not sure why this line gives me error
        self.treeview = tv
        self.treeview.pack(pady=5)

    def back_previous_page(self):
        image_to_text.list_of_dict = []
        self.controller.show_frame("PageOne")


# Created by Nigel
class FilterPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.image = Image.open("bgimg.gif")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.place(x=0, y=0)

        label = tk.Label(self, text="Filtered Result", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        back_previous_bt = tk.Button(self, text="Back", highlightbackground='#3E4149',
                                     command=lambda: self.controller.show_frame("PageOne"))
        back_previous_bt.place(x=5, y=12)

        print(GUI.filtered_output)

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
            # print("result is " + result)
            self.treeview.insert('', 'end', text=result2[0], values=(result2[1]))
