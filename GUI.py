import tkinter as tk
import boto3
import ImageToText
import LoginCheck
import DBAccessKey

from tkinter import *
from tkinter import filedialog
from tkinter import font as tk_font
from tkinter.ttk import *
from boto3.dynamodb.conditions import Key, Attr
from PIL import ImageTk, Image


access_key_id_global = DBAccessKey.DBAccessKey.access_key_id_global
secret_access_key_global = DBAccessKey.DBAccessKey.secret_access_key_global


class GUI:

    def __init__(self):
        self.master = Tk()
        self.master.minsize(500, 500)
        self.master.title("ME CFS")
        self.title_font = tk_font.Font(family='Helvetica', size=18, weight="bold")
        self.frames = {}

        container = tk.Frame(self.master)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Assign Pages
        frame = StartPage(parent=container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")

        # Add to frames list
        self.frames[StartPage.__name__] = frame

        # Show StartPage
        self.show_frame("StartPage", self.frames)

    def show_frame(self, page_name, frames):
        frame = frames[page_name]
        frame.tkraise()

    def back_previous_page(self, frames):
        ImageToText.list_of_dict = []
        self.show_frame("PageOne", frames)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.frames = controller.frames
        self.image = Image.open("Image/background_image.gif")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.place(x=0, y=0)

        label = tk.Label(self, text="Welcome to ME/CFS", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        usnm_lb = tk.Label(self, text="Username")
        usnm_lb.pack()
        usnm_lb.place(x=120, y=70)
        self.username_entry = Entry(self, width=24)
        self.configure(highlightthickness=0, highlightbackground="black", borderwidth=0)
        self.username_entry.place(x=190, y=70)

        password_lb = tk.Label(self, text="Password")
        password_lb.place(x=120, y=110)
        self.password_entry = Entry(self, show="*", width=24)
        self.password_entry.place(x=190, y=110)

        button_login = tk.Button(self, text="Login", highlightbackground='#3E4149',
                                 command=self.check_password)
        button_login.place(x=230, y=140)

    def check_password(self):
        username_to_check = self.username_entry.get()
        password_to_check = self.password_entry.get()
        login_checker = LoginCheck.LoginCheck(username_to_check, password_to_check)
        if login_checker.check_login():
            # Show page one
            frame = PageOne(parent=self.parent, controller=self.controller)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[PageOne.__name__] = frame
            self.controller.show_frame("PageOne", self.frames)
        else:
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.frames = controller.frames
        self.image = Image.open("Image/background_image.gif")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.place(x=0, y=0)

        label = tk.Label(self, text="Image Upload", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.name = ()

        ''' Open button - To select file
        '''
        self.openButton = tk.Button(self, text='Open', highlightbackground='#3E4149', command=self.open_file)
        self.openButton.place(x=180, y=140)
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
                           command=lambda: self.get_filtered_values(self.filter_entry.get()))

        button.place(x=230, y=230)

    def callback(self, name):
        print("callback name")
        print(name)
        object_img2txt = ImageToText.ImageToText(name)
        object_img2txt_output = object_img2txt.print_filename()
        print(object_img2txt_output)

        frame = PageTwo(parent=self.parent, controller=self.controller, object_img2txt_output=object_img2txt_output)
        self.frames[PageTwo.__name__] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.controller.show_frame("PageTwo", self.frames)

    def open_file(self):
        self.master.filename = filedialog.askopenfilenames(initialdir="/", title="Select file",
                                                           filetypes=(("png files", "*.png"), ("all files", "*.*")))
        print(self.master.filename)
        self.name = self.master.filename
        print("open file", self.name)
        self.fn_entry.set(self.name)

    def get_filtered_values(self, ref_no):

        database = boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id=access_key_id_global,
                                  aws_secret_access_key=secret_access_key_global)
        table = database.Table('ME_CFS_DB')

        response = table.query(
            KeyConditionExpression=Key('Reference_No').eq(ref_no)
        )

        filtered_output = []
        if response['Items']:
            for i in response['Items']:
                if i['Reference_No'] == ref_no:
                    for key in i.keys():
                        each_line = key + ": " + str(i[key])
                        filtered_output.append(each_line)
            frame = FilterPage(parent=self.parent, controller=self.controller, filtered_output=filtered_output)
            self.frames[FilterPage.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.controller.show_frame("FilterPage", self.frames)
        else:
            self.filter_entry.set("Invalid Reference No.")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller, object_img2txt_output):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.frames = controller.frames
        self.object_img2txt_output = object_img2txt_output
        self.image = Image.open("Image/background_image.gif")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.place(x=0, y=0)

        label = tk.Label(self, text="Result page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.file_lstbx = Listbox(self)
        self.file_lstbx.pack()

        count = 0
        for file_name in self.object_img2txt_output:  #  name should be dictionary rather than file name
            count = count + 1
            short_filename = file_name["filename"].split('/')
            filename_display = short_filename[-1]
            self.file_lstbx.insert(count, filename_display)

        self.file_lstbx.bind('<<ListboxSelect>>', self.display_selected_file)
        self.file_lstbx.pack()
        #cyoung12 self.createTable()
        submit_to_dbs_button = tk.Button(self, text="Upload", highlightbackground='#3E4149',
                                         command=lambda: self.DBS_upload())
        submit_to_dbs_button.place(x=400, y=12)

        back_previous_bt = tk.Button(self, text="Back", highlightbackground='#3E4149',
                                     command=lambda: self.controller.back_previous_page(self.frames))

        back_previous_bt.place(x=5, y=12)
        self.createTextBox()

    def insert_values(self, display_dict):
        '''self.treeview.delete(*self.treeview.get_children())
        self.treeview.destroy()
        self.createTable()
        self.result_dict = display_dict
        for result in self.result_dict.items():
            id = self.treeview.insert('', 'end', text=result[0], values=(result[1])) '''

            ##cyoung12 this is where the result was inserted

        #root = tk.Tk()
        '''S = tk.Scrollbar(self)
        T = tk.Text(self, height=10, width=60)
        T.place(x=100,y=100)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        T.pack(side=tk.LEFT, fill=tk.Y)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)'''
        #self.S.destroy()
        #self.T.destroy()
        self.T.delete('1.0', END)
        displayvalues=""
        for result in display_dict.items():
            displayvalues = displayvalues+"\n"+result[0]+"  "+result[1]
            #displayvalues = displayvalues + "\n" + result[0] + " : " + result[1]
        self.T.insert(tk.END, displayvalues)
        print("The output is :", self.T.get("1.0", END))


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
        hex_representation=  int(str(rowid).replace('I', ''), 16)

        rn = int(hex_representation)
        cn = int(str(columnid).replace('#', ''))

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
            entryedit.destroy()
            confirm_button.destroy()

        confirm_button = tk.Button(self, text='OK', width=4, command=saveedit)
        confirm_button.place(x=455 + (cn - 1) * 242, y=240 + rn * 20)#TODO set ok button to match scrolled position

    def DBS_upload(self):
        stringlist = ""
        fulllist = self.T.get("1.0", END)
        for i in fulllist:
            stringlist = stringlist+i
        stringlist = stringlist.splitlines()
        list_of_dict = {}
        field_str_list = ['Sodium', 'Potassium', 'Chloride', 'Bicarbonate', 'Urea', 'Creatinine', 'eGFR', 'T.Protein',
                          'Albumin', 'ALP', 'Bilirubin', 'GGT',
                          'AST', 'ALT', 'HAEMOGLOBIN', 'RBC', 'PCV', 'MCV', 'MCHC', 'RDW', 'wcc', 'Neutrophils',
                          'Lymphocytes', 'Monocytes',
                          'Eosinophils', 'Basophils', 'PLATELETS', 'ESR','Reference_No','Date_Time']
        print("pattern matching")
        for lines in stringlist:
            #print("Lines:",lines)
            for field_str in field_str_list:
                #print("List of item:",field_str)
                if(field_str in lines):
                    value = ImageToText.ImageToText.extract_value(lines,field_str)
                    list_of_dict[field_str]=value
                    #print(field_str+"::"+value)

                if ('MCH' in lines) and not ('MCHC' in lines):
                    MCH = ImageToText.ImageToText.extract_value(lines, 'MCH')
                    list_of_dict['MCH']=MCH
                    #print("MCH::>" + MCH)

        boolean_val = ImageToText.ImageToText.check_entry_exist(list_of_dict['Reference_No'])
        print("if that entry already exist:", boolean_val)
        if (boolean_val):
            print("Update it")
            # update it only
            for val in list_of_dict:
                if (val != 'Reference_No' and val != 'Date_Time'):
                    print("Resuld_dict:", val, " value:", list_of_dict[val])
                    val1 = val.replace('.', '_')
                    ImageToText.ImageToText.update_db(val1, list_of_dict[val], list_of_dict['Reference_No'],
                                                      list_of_dict['Date_Time'])

        else:
            print("Create it")
            # create it and update it
            ImageToText.ImageToText.write_to_db(list_of_dict['Reference_No'], list_of_dict['Date_Time'])
            for val in list_of_dict :
                if (val != 'Reference_No' and val != 'Date_Time'):
                    print("Resuld_dict:", val, " value:", list_of_dict[val])
                    val1 = val.replace('.', '_')
                    ImageToText.ImageToText.update_db(val1, list_of_dict[val], list_of_dict['Reference_No'],
                                                      list_of_dict['Date_Time'])


        '''print("in DBS_upload:", self.result_dict)
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
                                                        self.result_dict['Date_Time']) '''

    def display_selected_file(self, event):
        if self.file_lstbx.curselection():
            idx = (self.file_lstbx.curselection()[0])
            display_dict = self.object_img2txt_output[idx]
            #self.treeview.delete(*self.treeview.get_children())
            self.insert_values(display_dict)

    def createTextBox(self):
        self.S = tk.Scrollbar(self)
        xscrollbar = Scrollbar(self, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)
        self.T = tk.Text(self, wrap=NONE, height=10, width=50)
        self.T.place(x=100, y=100)
        self.S.pack(side=tk.RIGHT, fill=tk.Y)
        self.T.pack(side=tk.LEFT, fill=tk.Y)
        xscrollbar.config(command=self.T.xview)
        self.S.config(command=self.T.yview)
        self.T.config(xscrollcommand=xscrollbar.set)
        self.T.config(yscrollcommand=self.S.set)


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

        self.treeview = tv
        self.treeview.pack(pady=5)


class FilterPage(tk.Frame):

    def __init__(self, parent, controller, filtered_output):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.frames = controller.frames
        self.filtered_output = filtered_output
        self.image = Image.open("Image/background_image.gif")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.place(x=0, y=0)

        label = tk.Label(self, text="Filtered Result", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_previous_bt = tk.Button(self, text="Back", highlightbackground='#3E4149',
                                     command=lambda: self.controller.back_previous_page(self.frames))
        back_previous_bt.place(x=5, y=12)
        self.create_filter_table(self.filtered_output)

    def create_filter_table(self, filtered_output):
        tv = Treeview(self, height=20)
        tv['columns'] = 'values'
        tv.heading("#0", text='Attributes', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('values', text='Values')
        tv.column('values', anchor='center', width=50)
        vsb = tk.Scrollbar(tv, orient="vertical", command=tv.yview)
        vsb.place(x=387, y=0, height=30)
        tv.configure(yscrollcommand=vsb.set)
        tv.pack(pady=5)
        for result in filtered_output:
            result2 = result.split(": ")
            tv.insert('', 'end', text=result2[0], values=(result2[1]))
