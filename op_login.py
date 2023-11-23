import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import parkin_credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage

class OperatorLoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ParkIn- Operator Login Page")
        self.geometry("900x900")

        # Frame Dimensions and Placement
        self.frame_width = 0.4
        self.frame_height = 0.6
        self.relx = (1 - self.frame_width) / 2
        self.rely = (1 - self.frame_height) / 2

        # Creating Frame
        self.frame = tk.Frame(self, bg="white", bd=4)
        self.frame.place(relx=self.relx, rely=self.rely, relwidth=self.frame_width, relheight=self.frame_height)

        # Label for Login
        self.label = tk.Label(self.frame, text="Login", bg="white", fg="black", anchor="w", font=("Verdana", 16))
        self.label.pack(side="top", anchor="w", padx=10, pady=10)

        # Username Entry Field
        self.username_label = tk.Label(self.frame, text="Username", bg="white", fg="black")
        self.username_label.pack(anchor="w", padx=10, pady=15)

        self.username_entry = tk.Entry(self.frame, fg="grey", bg="white", width=50)
        self.username_entry.insert(0, "Enter Username")
        self.username_entry.bind("<FocusIn>", self.on_entry_click_username)
        self.username_entry.bind("<FocusOut>", self.on_entry_leave_username)
        self.username_entry.pack(anchor="w", padx=10, pady=5)

        # Password Entry Field
        password_label = tk.Label(self.frame, text="Password", bg="white", fg="black")
        password_label.pack(anchor="w", padx=10, pady=15)

        self.show_password = tk.BooleanVar()
        self.show_password.set(False)

        self.password_entry = tk.Entry(self.frame, fg="grey", bg="white", width=50)
        self.password_entry.insert(0, "Enter Password")
        self.password_entry.bind("<FocusIn>", self.on_entry_click_password)
        self.password_entry.bind("<FocusOut>", self.on_entry_leave_password)
        self.password_entry.pack(anchor="w", padx=10, pady=5)

        # Show Password
        toggle_password_button = tk.Checkbutton(self.frame, text="Show Password", bg="white", variable=self.show_password, command=self.toggle_password_visibility)
        toggle_password_button.pack(anchor="w", padx=10, pady=5)

        # Login Button
        login_button = tk.Button(self.frame, text="Login Now", font=("Verdana", 12), fg="white", width=20, bg="grey", command=self.login_func)
        login_button.pack(side="bottom", pady=10, fill='x')  # Filling the width of the frame

        # Forgot Password Button
        forgot_password_button = tk.Button(self.frame, text="Forgot Password?", font=("Verdana", 10), fg="blue", command=self.forgot_password)
        forgot_password_button.pack(side="bottom", anchor="w", padx=8, pady=5)

        # Go to Registration Page Link
        reg_link = tk.Label(self.frame, text="Don't have an account yet? Sign up", bg="white", font=("Verdana", 8, "underline"), fg="blue")
        reg_link.pack(side="bottom", padx=10, pady=10)
        reg_link.bind("<Button-1>", self.opreg_window)

    # ... (rest of your class methods)

    

        
        
    def on_entry_click_username(self,event):
        if self.username_entry.get()=="Enter Username":
            self.username_entry.delete(0,"end")
            self.username_entry.config(show="")
            self.username_entry.config(fg="black")
            
    def on_entry_leave_username(self,event):
        if self.username_entry.get()=="":
            self.username_entry.insert(0,"Enter Username")
            self.username_entry.config(fg="grey")
            
    def on_entry_click_password(self, event):
        if self.password_entry.get() == "Enter Password":
            self.password_entry.delete(0, "end")
            self.password_entry.config(show="")
            self.password_entry.config(fg="black")

    def on_entry_leave_password(self, event):
        if self.password_entry.get() == "":
            self.password_entry.insert(0, "Enter Password")
            self.password_entry.config(fg="grey")
        elif self.password_entry.get() == "Enter Password":
            self.password_entry.delete(0, "end")
            self.password_entry.config(show="*")
            self.password_entry.config(fg="black")
            
    def toggle_password_visibility(self):
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def opreg_window(self,event):
        self.destroy()
        subprocess.Popen(["python3","/Users/tulasirambommisetty/Downloads/done_so_far/op_reg.py"])
        
    def login_func(self):
        if self.username_entry.get()=="" or self.password_entry.get()=="":
            messagebox.showerror("Error!","All fields are required")
        else:
            try:
                connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()
                username=self.username_entry.get()  
                password=self.password_entry.get()  
                
                #CHECK IF USERNAME EXISTS
                query1="SELECT * FROM Operator WHERE Operatorname=%s"
                cur.execute(query1,(username,))
                row=cur.fetchone()
                if row is None:
                    messagebox.showerror("Error!","Username does not exist. Please register.")
                else:
                    #CHECK IF PASSWORD MATCHES USERNAME
                    query2="SELECT Password FROM Operator WHERE Operatorname=%s"
                    cur.execute(query2,(username,))
                    res=cur.fetchone()
                    correct_pass=res[0]
                    print(correct_pass)
                    print(password)
                    if password!=correct_pass:
                        messagebox.showerror("Error!","Incorrect Password.")
                    else:
                        messagebox.showinfo("Success","Welcome Back!")
                        
                        #PASS O_ID TO NEXT PAGE
                        cur = connection.cursor()
                        query2 = "SELECT O_id FROM Operator WHERE Operatorname = %s"
                        cur.execute(query2, (username,))
                        result = cur.fetchone()
                        O_id=str(result[0])
                        self.reset_fields()
                        connection.close()
                        self.destroy()
                        subprocess.Popen(["python3","/Users/tulasirambommisetty/Downloads/done_so_far/op_home_page.py",O_id])
            except Exception as e:
                messagebox.showerror("Error!", f"Error due to {str(e)}")

    def reset_fields(self):
        self.username_entry.delete(0, "end")
        self.username_entry.insert(0, "Enter Username")
        self.username_entry.config(fg="grey")
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, "Enter Password")
        self.password_entry.config(fg="grey")
        self.show_password.set(False)


    def forgot_password(self):
        username = self.username_entry.get()
        if not username or username == "Enter Username":
            messagebox.showerror("Error!", "Please enter your username to reset the password.")
        else:
            try:
                connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()

                # CHECK IF USERNAME EXISTS
                query = "SELECT * FROM Operator WHERE Operatorname=%s"
                cur.execute(query, (username,))
                row = cur.fetchone()

                if row is None:
                    messagebox.showerror("Error!", "Username does not exist. Please register.")
                else:
                    # Generate a new password (you may want a more secure method)
                    new_password = "new_generated_password"

                    # Update the password in the database for the given username
                    update_query = "UPDATE Operator SET Password = %s WHERE Operatorname = %s"
                    cur.execute(update_query, (new_password, username))
                    connection.commit()

                    messagebox.showinfo("Password Reset", f"Password reset successful for {username}. Your new password is: {new_password}")
                    connection.close()

            except Exception as e:
                messagebox.showerror("Error!", f"Error due to {str(e)}")
        
if __name__ == "__main__":
    app = OperatorLoginPage()
    app.mainloop()

            
  
