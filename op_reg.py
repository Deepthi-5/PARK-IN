import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import datetime
import mysql.connector
import subprocess
import parkin_credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
class OpRegistrationPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ParkIn- Operator Registration Page")
        self.geometry("900x600")
        #self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        #background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        #self.eval('tk::PlaceWindow . center')

        self.frame = tk.Frame(self, bg="white", bd=4)
        self.frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        self.label = tk.Label(self.frame, text="Register", bg="white", anchor="w", font=("Verdana", 16))
        self.label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        #CREATE ENTRY FIELDS

        self.entry_dict = {}
        self.entries1 = ["Username", "Password","Phone","Email"]
        self.entries3 = ["Location","Floors","Slots per Floor", "Rate per hour"]
        self.create_entry_fields(self.entries1, column=0)
        self.create_entry_fields(self.entries3, column=1)
        for col in range(3):
            self.frame.grid_columnconfigure(col, weight=1)

        #SIGN UP BUTTON
        signup_button = tk.Button(self.frame, text="Sign Up", font=("Verdana", 12), fg="white", width=20, bg="Grey", command=self.signup_func)
        signup_button.grid(row=len(self.entries1) + 20, column=0, padx=10, pady=25, columnspan=2)
        
        #GO TO LOGIN PAGE
        log_link = tk.Label(self.frame, text="Already have an account? Login", bg="white", font=("Verdana", 8, "underline"), fg="blue")
        log_link.grid(row=len(self.entries1) + 22, column=0, padx=10, pady=10, columnspan=2)
        log_link.bind("<Button-1>", self.oplogin_window)
   
    def create_entry_fields(self, entries, column):
        for i, entry_text in enumerate(entries):
            label_row = i * 2 + 2  
            entry_row = label_row + 1
    
            label = tk.Label(self.frame, text=entry_text, bg="white")
            label.grid(row=label_row, column=column, padx=10, pady=5, sticky="w")
            
            entry = tk.Entry(self.frame, fg="grey", width=30)
            entry.grid(row=entry_row, column=column, padx=10, pady=5, sticky="w")
            entry.insert(0,f"Enter {entry_text}")
            self.setup_placeholder(entry, f"Enter {entry_text}")
            

    def setup_placeholder(self, entry, placeholder):
        self.entry_dict[entry] = placeholder
        if isinstance(entry, tk.Entry):
            entry.bind("<FocusIn>", self.on_entry_click)
            entry.bind("<FocusOut>", self.on_entry_leave)
        elif isinstance(entry, tk.Text):
            entry.bind("<FocusIn>", self.on_text_click)
            entry.bind("<FocusOut>", self.on_text_leave)
            
    def on_entry_click(self, event):
        entry = event.widget
        if entry.get() == self.entry_dict[entry]:
            entry.delete(0,"end")
            entry.config(fg="black")

    def on_entry_leave(self, event):
        entry = event.widget
        if entry.get().strip() == "":    
            entry.delete(0, "end")
            entry.insert(0, self.entry_dict[entry])
            entry.config(fg="grey")
          
    def on_text_click(self, event):
        text = event.widget
        if text.get("1.0", "end-1c") == self.entry_dict[text]:
            text.delete("1.0", "end-1c")
            text.config(fg="black")

    def on_text_leave(self, event):
        text = event.widget
        if text.get("1.0", "end-1c").strip() == "":
            text.delete("1.0", "end-1c")
            text.insert("1.0", self.entry_dict[text])
            text.config(fg="grey")
            
    def oplogin_window(self,event):
        self.destroy()
        subprocess.Popen(["python","op_login.py"])
   
        
    def signup_func(self):
            #CHECK IF ALL FIELDS ARE FILLED
            validation_result = self.validate_entries()
            
            #GET THE INPUT FROM ALL FIELDS
            if validation_result:
                connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()
                for entry, placeholder in self.entry_dict.items():
                    if isinstance(entry, tk.Entry):
                        if placeholder == "Enter Username":
                            username = entry.get()
                        elif placeholder == "Enter Password":
                                password = entry.get()
                        elif placeholder == "Enter Phone":
                                phone = entry.get()
                        elif placeholder == "Enter Email":
                                email = entry.get()
                        elif placeholder == "Enter Location":
                                location = entry.get()
                        elif placeholder == "Enter Rate per hour":
                                rate = entry.get()
                        elif placeholder == "Enter Floors":
                                floors = entry.get()
                        elif placeholder == "Enter Slots per Floor":
                                slots = entry.get()

                #CHECK IF INPUTS ARE VALID
                validation_errors = [] 
                validation_errors = self.validation_error(validation_errors,username,password,phone,email,rate,floors,slots,location)
                if validation_errors:
                    try:
                        curr_date=datetime.date.today()
                        #DOJ= str(datetime.date.today().strftime('%Y-%m-%d'))
                        rate=str(rate)

                        #PERFORM INSERTION
                        query1 = "INSERT INTO Operator (Operatorname, Password, Location, Phone, Email,Floors, slot_per_floor, Rate_per_hour) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                        cur.execute(query1, (username, password, location, phone, email, floors,slots, rate))
                
                        #PASS O_ID TO NEXT PAGE
                        query2 = "SELECT O_id FROM Operator WHERE Operatorname = %s"
                        cur.execute(query2, (username,))
                        result = cur.fetchone()
                        O_id=str(result[0])
                        
                        connection.commit() 
                        #INSERT INTO SLOT MANAGEMENT TABLE
                        for i in range(1,int(floors)+1):
                            for j in range (1,int(slots)+1):
                                query= "INSERT INTO Slot_Management (O_id, Floor_no, Slot_no, Occupancy) VALUES (%s, %s, %s, 0)"
                                cur.execute(query, (O_id, i, j))
                                connection.commit() 
                                
                        connection.commit() 

                        connection.close()
                        self.destroy()
                        subprocess.Popen(["python", "op_home_page.py", O_id])
                    except Exception as e:
                        connection.rollback()  
                        messagebox.showerror("Error", f"Error due to {str(e)}")
                    
                        
                        
                        
    def validation_error(self,validation_errors,username,password,phone,email,rate,floor,slots,location):
         if len(username) < 3:
              messagebox.showerror("Error!", "Username is too short. It must have a length of at least 3.")
              return False
         connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
         cur = connection.cursor()
         query1= "SELECT * FROM Operator WHERE Operatorname = %s"
         cur.execute(query1,(username,))
         result = cur.fetchall()
         if result:
                  messagebox.showerror("Error!", "Username already exists.")
                  connection.close()
                  return False
         if len(password) < 5:
              messagebox.showerror("Error!", "Password is too short. It must have a length of at least 5.")
              return False
         if not location.replace(" ", "").isalpha():
              messagebox.showerror("Error!", "Location should contain only alphabets.")
              return False
         if not phone.isnumeric():
              messagebox.showerror("Error!","Phone number should contain only numerals.")
              return False
         if len(phone)!=10:
             messagebox.showerror("Error!","Please enter a valid Phone.")
             return False
         if not floor.isnumeric():
              messagebox.showerror("Error!","No. of floors must be a numerals.")
              return False
         if len(floor)>2:
             messagebox.showerror("Error!","Sorry, Our database does not currently support these many floors.")
             return False
         if not slots.isnumeric():
              messagebox.showerror("Error!","No. of slots per floor must be a numerals.")
              return False
         if len(slots)>2:
             messagebox.showerror("Error!","Sorry, Our database does not currently support these many slots.")
             return False
         
         email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
         if not re.match(email_pattern, email):
              messagebox.showerror("Error!", "Please enter a valid email address.")
              return False
         try:
              rate = float(rate)
              if not (0 <= rate <= 9999999.99):
                  messagebox.showerror("Error!", "Rate has exceeded the limit.")
                  return False
         except ValueError:
                 messagebox.showerror("Error!", "Please enter a valid rate per hour.")
                 return False
         return True
              
    def validate_entries(self):
        mandatory_fields = ["Enter Username",
                            "Enter Password", 
                            "Enter Location", 
                            "Enter Phone", 
                            "Enter Email", 
                            "Enter Floors", 
                            "Enter Slots per floor", 
                            "Enter Rate per hour"]   
        for entry, placeholder in self.entry_dict.items():
            if isinstance(entry, tk.Entry):
                if entry.get().strip() == placeholder and placeholder in mandatory_fields:
                    messagebox.showerror("Error!", f"{placeholder}")
                    return False 
        return True

    
if __name__ == "__main__":
     app = OpRegistrationPage()
     app.mainloop()    
     
