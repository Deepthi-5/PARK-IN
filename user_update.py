from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import os,sys
#from operator_details_page import OperatorDetailsPage
#from signup_page import SignUp
import parkin_credentials as cr
import subprocess
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage

class UserUpdate:
    def __init__(self, root,O_id):
        self.window = root
        self.window.title("Update User")
        self.U_id=O_id
        # Set the window size
        # Here 0,0 represents the starting point of the window 
        self.window.geometry("1280x800+0+0")
        self.window.config(bg = "white")
        
        self.frame1 = Frame(self.window, bg="#7DC5E7")
        self.frame1.place(x=0, y=0, width=450, relheight = 1)

        self.frame2 = Frame(self.window, bg = "#F0F8FF")
        self.frame2.place(x=450,y=0,relwidth=1, relheight=1)

        self.frame3 = Frame(self.frame2, bg="white")
        self.frame3.place(x=140,y=150,width=500,height=450)

        self.uname=StringVar()
        self.email=StringVar()
        self.pswd=StringVar()
        self.phno=StringVar()
        self.vno=StringVar()
        self.vtype=StringVar()

        self.fetch_data()

        stud_id_label=Label(self.frame3,text="Username",font=("times new roman",12,"bold"),padx=2,pady=6,fg="black",bg="white",width=10)
        stud_id_label.grid(row=1,column=1,sticky=W)
        self.entry_ref=ttk.Entry(self.frame3,width=20,textvariable=self.uname,font=("times new roman",12,"bold"))
        self.entry_ref.grid(row=1,column=2)

        stud_id_label=Label(self.frame3,text="Email",font=("times new roman",12,"bold"),padx=2,pady=6,fg="black",bg="white",width=10)
        stud_id_label.grid(row=2,column=1,sticky=W)
        self.entry_ref=ttk.Entry(self.frame3,width=20,textvariable=self.email,font=("times new roman",12,"bold"))
        self.entry_ref.grid(row=2,column=2)

        stud_id_label=Label(self.frame3,text="Password",font=("times new roman",12,"bold"),padx=2,pady=6,fg="black",bg="white",width=10)
        stud_id_label.grid(row=3,column=1,sticky=W)
        self.entry_ref=ttk.Entry(self.frame3,width=20,textvariable=self.pswd,font=("times new roman",12,"bold"))
        self.entry_ref.grid(row=3,column=2)

        stud_id_label=Label(self.frame3,text="Phone No",font=("times new roman",12,"bold"),padx=2,pady=6,fg="black",bg="white",width=10)
        stud_id_label.grid(row=4,column=1,sticky=W)
        self.entry_ref=ttk.Entry(self.frame3,width=20,textvariable=self.phno,font=("times new roman",12,"bold"))
        self.entry_ref.grid(row=4,column=2)

        stud_id_label=Label(self.frame3,text="Vehicle No",font=("times new roman",12,"bold"),padx=2,pady=6,fg="black",bg="white",width=10)
        stud_id_label.grid(row=5,column=1,sticky=W)
        self.entry_ref=ttk.Entry(self.frame3,width=20,textvariable=self.vno,font=("times new roman",12,"bold"))
        self.entry_ref.grid(row=5,column=2)

        stud_id_label=Label(self.frame3,text="Vehicle Type",font=("times new roman",12,"bold"),padx=2,pady=6,fg="black",bg="white",width=10)
        stud_id_label.grid(row=6,column=1,sticky=W)
        self.entry_ref=ttk.Entry(self.frame3,width=20,textvariable=self.vtype,font=("times new roman",12,"bold"))
        self.entry_ref.grid(row=6,column=2)

        upd_btn=Button(self.frame3,text="Update",command=self.update_data,font=("arial",12,"bold"),fg="black",bg="white",width=30)
        upd_btn.grid(row=8,column=2,padx=5,pady=20)

    def fetch_data(self):
        connection=mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        print(self.U_id)
        cur.execute("select * from User where U_id=%s",(self.U_id,))
        row=cur.fetchone()
        print(row)
        if row:
            # Update the StringVar objects with the fetched data
            self.uname.set(row[1])  
            self.email.set(row[2])  
            self.pswd.set(row[3])  
            self.phno.set(row[4])   
            self.vno.set(row[5])    
            self.vtype.set(row[6])  
        connection.close()

    def update_data(self):        
        connection=mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        cur.execute("update User set Username=%s,Email=%s,Password=%s,Phone=%s,V_no=%s,V_type=%s where U_id=%s",(
                self.uname.get(),
                self.email.get(),
                self.pswd.get(),
                self.phno.get(),
                self.vno.get(),
                self.vtype.get(),
                self.U_id
                ))  
        connection.commit()  
        connection.close()
        messagebox.showinfo("Success","Updated successfully!")

# The main function
if __name__ == "__main__":
    '''O_id = sys.argv[1] if len(sys.argv) > 1 else None
    if O_id is not None:
        O_id = str(O_id)'''
    root = Tk()
    O_id="111"
    obj = UserUpdate(root,O_id)
    root.mainloop()



'''import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import parkin_credentials as cr
import subprocess,sys
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage

class UserUpdate():
    def __init__(self, root):
        self.window = root
        self.window.title("Update user details")
        # Set the window size
        # Here 0,0 represents the starting point of the window 
        self.window.geometry("1280x800+0+0")
        self.window.config(bg = "white")
        #self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        #background = Label(self.window,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)

        self.frame1 = tk.Frame(self.window, bg="#7DC5E7")
        self.frame1.place(x=0, y=0, width=450, relheight = 1)

        self.frame2 = tk.Frame(self.window, bg = "#F0F8FF")
        self.frame2.place(x=450,y=0,relwidth=1, relheight=1)

        self.frame3 = tk.Frame(self.frame2, bg="white")
        self.frame3.place(x=140,y=150,width=500,height=450)

        self.svar_genderv=tk.StringVar()
        self.qevv=tk.StringVar()
        self.hstv=tk.StringVar()
        self.gvar_genderv=tk.StringVar()
        self.alumv=tk.StringVar()
        self.srnv=tk.StringVar()
        self.fnamev=tk.StringVar()
        self.mnamev=tk.StringVar()
        self.lnamev=tk.StringVar()
        self.dobv=tk.StringVar()

        self.uname_label = tk.Label(self.frame3,text="Username", font=("helvetica",20,"bold"),bg="white", fg="gray").place(x=50,y=40)
        self.uname_entry = tk.Entry(self.frame3,font=("times new roman",15,"bold"),bg="white",fg="gray")
        self.uname_entry.place(x=50, y=80, width=300)

'''
if __name__=="_main_":
    #O_id = sys.argv[1] if len(sys.argv) > 1 else None
    #if O_id is not None:
    #    O_id = str(O_id)
    O_id="1"
    root = tk.Tk()
    obj = UserUpdate(root)
    root.mainloop()
    