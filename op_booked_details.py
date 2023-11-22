import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import parkin_credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
import sys

class UserDetails(tk.Tk):
    def __init__(self,O_id,U_id):
        super().__init__()
        self.title("ParkIn- User Details")
        self.geometry("900x600")
        
        self.header_label = tk.Label(self, text="User Details", font=("Verdana", 16))
        self.header_label.place(relx=0.5, rely=0.01, anchor="n")
        
        self.back_button = tk.Button(self, text="<- Back", font=("Verdana", 10),command=self.go_to_home)
        self.back_button.place(relx=0.1, rely=0.01, anchor="n")
        
        self.frame = tk.Frame(self, bg="white", bd=4)
        self.frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        
        self.payment_button = tk.Button(self.frame, text="Manage Payment", font=("Verdana", 12),command=self.payment_manage)
        self.payment_button.grid(row=10, column=0, padx=20, pady=5, sticky="w")
        
        # Fetch and display user information
        user_info = self.fetch_user_info(U_id)
        self.display_user_info(user_info)

    def fetch_user_info(self, U_id):
       try:
           connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
           with connection.cursor() as cursor:
               # Execute the SELECT query
               query = f"SELECT * FROM User WHERE U_id = %s"
               cursor.execute(query,(str(U_id),))
               
               # Fetch the user information
               user_info = cursor.fetchone()
               
               return user_info

       except Exception as e:
           print(f"Error: {e}")
       finally:
           connection.close()

    def display_user_info(self, user_info):
       if user_info:
           labels = ["U_id", "Username", "Email", "Password", "Phone", "V_no", "V_type"]
           
           for i, label_text in enumerate(labels):
               label = tk.Label(self.frame, text=f"{label_text}: {user_info[i]}", font=("Verdana", 12), anchor="w")
               label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
        
        
        
    def payment_manage(self):
        subprocess.Popen(["python", "op_payment.py", O_id])  
        self.destroy()

    def go_to_home(self):
         subprocess.Popen(["python", "op_home_page.py", O_id])  
         self.destroy()
         
if __name__ == "__main__":
    #O_id = sys.argv[1] if len(sys.argv) > 1 else None
    #U_id = sys.argv[2] if len(sys.argv) > 1 else None
    #if U_id and O_id is not None:
    #    U_id = str(U_id)
    #    O_id=str(O_id)
    O_id="1"
    U_id="1"
    app = UserDetails(O_id,U_id)
    app.mainloop()
