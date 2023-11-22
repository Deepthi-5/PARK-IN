from tkinter import *
import mysql.connector
import tkinter as tk
from tkinter import messagebox
import parkin_credentials as cr
import sys

class UserRegPage(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.window = root
        #self.window.title("User Registration")
        #self.window.geometry("1280x800+0+0")
        #self.window.config(bg="white")
        self.title("User Registration")
        self.geometry("1280x800+0+0")
        self.config(bg="white")
        

        self.frame1 = Frame(self, bg="#7DC5E7")
        self.frame1.place(x=0, y=0, width=450, relheight=1)

        self.frame2 = Frame(self, bg="#F0F8FF")
        self.frame2.place(x=450, y=0, relwidth=1, relheight=1)

        self.frame3 = Frame(self.frame2, bg="white")
        self.frame3.place(x=140, y=150, width=500, height=450)

        self.username_entry = Entry(self.frame3, font=("times new roman", 12))
        self.username_entry.place(x=200, y=40, width=250)

        self.email_entry = Entry(self.frame3, font=("times new roman", 12))
        self.email_entry.place(x=150, y=80, width=300)

        self.password_entry = Entry(self.frame3, font=("times new roman", 12), show='*')
        self.password_entry.place(x=200, y=120, width=250)

        self.phone_entry = Entry(self.frame3, font=("times new roman", 12))
        self.phone_entry.place(x=150, y=160, width=300)

        self.vehicle_no_entry = Entry(self.frame3, font=("times new roman", 12))
        self.vehicle_no_entry.place(x=150, y=200, width=300)

        self.label_username = Label(self.frame3, text="Username", font=("helvetica", 20, "bold"), bg="white", fg="gray")
        self.label_username.place(x=50, y=40)

        self.label_email = Label(self.frame3, text="Email", font=("helvetica", 20, "bold"), bg="white", fg="gray")
        self.label_email.place(x=50, y=80)

        self.label_password = Label(self.frame3, text="Password", font=("helvetica", 20, "bold"), bg="white", fg="gray")
        self.label_password.place(x=50, y=120)

        self.label_phone = Label(self.frame3, text="Phone", font=("helvetica", 20, "bold"), bg="white", fg="gray")
        self.label_phone.place(x=50, y=160)

        self.label_vehicle_no = Label(self.frame3, text="Vehicle No", font=("helvetica", 20, "bold"), bg="white", fg="gray")
        self.label_vehicle_no.place(x=50, y=200)

        self.label_vehicle_type = Label(self.frame3, text="Vehicle Type", font=("helvetica", 20, "bold"), bg="white", fg="gray")
        self.label_vehicle_type.place(x=50, y=240)

        self.signup_button = Button(self.frame3, text="Sign Up", command=self.signup, font=("times new roman", 18, "bold"), bd=0, cursor="hand2", bg="#71A6D2", fg="white")
        self.signup_button.place(x=80, y=320, width=250)

        self.vehicle_types = ['4-wheeler', '2-wheeler', 'Other']
        self.vehicle_type_var = StringVar(self)
        self.vehicle_type_var.set(self.vehicle_types[0])
        self.vehicle_type_dropdown = OptionMenu(self.frame3, self.vehicle_type_var, *self.vehicle_types)
        self.vehicle_type_dropdown.place(x=250, y=240, width=200)

    def signup(self):
        try:
            #connection = mysql.connector.connect(host='localhost', user='root', password='deepthi1600', database='PARKIN')
            connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cursor = connection.cursor()
            
            username = self.username_entry.get()
            email = self.email_entry.get()
            password = self.password_entry.get()
            phone = self.phone_entry.get()
            vehicle_no = self.vehicle_no_entry.get()
            vehicle_type = self.vehicle_type_var.get()

            cursor.execute("INSERT INTO User(Username, Email, Password, Phone, V_no, V_type) VALUES (%s, %s, %s, %s, %s, %s)",
                           (username, email, password, phone, vehicle_no, vehicle_type))
            connection.commit()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

        finally:
            if 'connection' in locals():
                messagebox.showinfo("Success", "Registered successfully!")
                #PASS O_ID TO NEXT PAGE
                query2 = "SELECT U_id FROM User WHERE Userrname = %s"
                cursor.execute(query2, (username,))
                result = cursor.fetchone()
                U_id=str(result[0])
                print(U_id)
                connection.close()
                self.destroy()
                subprocess.Popen(["python", "user_home.py", U_id])

"""if __name__ == "__main__":
    root = Tk()
    obj = UserRegPage(root)
    root.mainloop()"""

if __name__ == "__main__":
    app = UserRegPage()
    app.mainloop()
