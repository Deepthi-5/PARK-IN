import tkinter as tk
import subprocess
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage

class ParkInApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ParkIn-WelcomePage!")
        self.geometry("900x600")
        #self.eval('tk::PlaceWindow . center')
        #self.bg_img = ImageTk.PhotoImage(file="bg.jpg")
        #background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        
        self.header_label1 = tk.Label(self, text="Welcome to ParkIn!", font=("Verdana", 20))
        self.header_label1.place(relx=0.5, rely=0.1, anchor="n")
        self.header_label2= tk.Label(self, text="Which of the following best describes you?", font=("Times New Roman", 16))
        self.header_label2.place(relx=0.5, rely=0.2, anchor="n")
        
        #GO TO USER INTERFACE
        self.button1 = tk.Button(self, text="USER \n I am an individual who \n wants to search for \n available parking spaces", command=self.open_user, font=("Helvetica", 16))
        self.button1.place(relx=0.1, rely=0.3, relwidth=0.3, relheight=0.4)
        
        #GO TO Operator INTERFACE
        self.button2 = tk.Button(self, text="OPERATOR \n I am an organization \n offering my services", command=self.open_op, font=("Helvetica", 16))
        self.button2.place(relx=0.6, rely=0.3, relwidth=0.3, relheight=0.4)

    def open_user(self):
        self.destroy()
        subprocess.Popen(["python","user_login.py"])
    
    def open_op(self):
        self.destroy()
        subprocess.Popen(["python","op_login.py"])

        
if __name__=="__main__":
    app=ParkInApp()
    app.mainloop()

