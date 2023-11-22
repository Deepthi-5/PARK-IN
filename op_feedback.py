import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import sys
import mysql.connector
import parkin_credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
class MHPReview(tk.Tk):
    def __init__(self, O_id):
        super().__init__()
        self.title("ParkIn-Operator Feedback")
        self.geometry("900x600")
        #self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        #background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        #self.eval('tk::PlaceWindow . center')
        self.header_label = tk.Label(self, text="Feedbacks", font=("Verdana", 16))
        self.header_label.place(relx=0.5, rely=0.01, anchor="n")
        
        self.back_button = tk.Button(self, text="<- Back", font=("Verdana", 10),command=self.go_to_home)
        self.back_button.place(relx=0.1, rely=0.01, anchor="n")
        
        self.frame = tk.Frame(self, bg="white", bd=4)
        self.frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        self.label = tk.Label(self.frame, text="User Feedback", bg="white", font=("Verdana", 10))
        self.label.grid(row=0, column=0, padx=(5, 0), pady=5, sticky="w")
        
        
        #CANVAS FOR UPCOMING REQUESTS
        self.canvas = tk.Canvas(self.frame,width=675,height=340)
        self.canvas.grid(row=4, column=0,columnspan=2)
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=4, column=3, sticky="ns")
        scrollbar2 = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        scrollbar2.grid(row=17, column=0,columnspan=9, sticky="ew")
        self.inner_frame = tk.Frame(self.canvas,height=160)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.display_reviews()
        
    def display_reviews(self):
            connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            query= """SELECT U.Username, U.V_no, U.Phone, F.Comment, F.Date, F.Time
                        FROM Feedback F 
                        INNER JOIN User U ON F.U_id = U.U_id 
                        WHERE F.O_id = %s 
                        ORDER BY F.Date DESC, F.Time DESC;"""
            cur.execute(query, (str(O_id),))
            result=cur.fetchall()
            connection.close()
            self.display_result(result)
    
  
    def display_result(self,result):
        if result:
                header_label1 = tk.Label(self.inner_frame, text="Username",font=("Verdana", 10))
                header_label1.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")
                header_label2 = tk.Label(self.inner_frame, text="Vehicle No.",font=("Verdana", 10))
                header_label2.grid(row=1, column=2, padx=5, pady=5, columnspan=3, sticky="w")
                header_label3 = tk.Label(self.inner_frame, text="Phone No.",font=("Verdana", 10))
                header_label3.grid(row=1, column=3, padx=5, pady=5, columnspan=3, sticky="w")
                header_label4 = tk.Label(self.inner_frame, text="Comment",font=("Verdana", 10))
                header_label4.grid(row=1, column=4, padx=5, pady=5, columnspan=3, sticky="w")
                header_label5 = tk.Label(self.inner_frame, text="Date",font=("Verdana", 10))
                header_label5.grid(row=1, column=5, padx=5, pady=5, columnspan=3, sticky="w")
                header_label6 = tk.Label(self.inner_frame, text="Time",font=("Verdana", 10))
                header_label6.grid(row=1, column=6, padx=5, pady=5, columnspan=3, sticky="w")
                row_no=2
                for row in result:
                    label1 = tk.Label(self.inner_frame, text=f"{row[0]}", bg="white",font=("Verdana", 10))
                    label1.grid(row=row_no, column=0, padx=5, pady=5, rowspan=2, sticky="w")
                    label2 = tk.Label(self.inner_frame, text=f"{row[1]}", bg="white",font=("Verdana", 10))
                    label2.grid(row=row_no, column=2, padx=5, pady=5, rowspan=2, sticky="w")
                    label3 = tk.Label(self.inner_frame, text=f"{row[2]}", bg="white",font=("Verdana", 10))
                    label3.grid(row=row_no, column=3, padx=5, pady=5, rowspan=2, sticky="w")
                    label4 = tk.Label(self.inner_frame, text=f"{row[3]}", bg="white",font=("Verdana", 10))
                    label4.grid(row=row_no, column=4, padx=5, pady=5, rowspan=2, sticky="w")
                    label5 = tk.Label(self.inner_frame, text=f"{row[4]}", bg="white",font=("Verdana", 10))
                    label5.grid(row=row_no, column=5, padx=5, pady=5, rowspan=2, sticky="w")
                    label6 = tk.Label(self.inner_frame, text=f"{row[5]}", bg="white",font=("Verdana", 10))
                    label6.grid(row=row_no, column=6, padx=5, pady=5, rowspan=2, sticky="w")
                    row_no+=2   
        else:
                no_appointments_label = tk.Label(self.inner_frame, text="No Feedbacks yet :)", font=("Verdana", 10))
                no_appointments_label.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w") 
        
        
                
    def on_click(self):
        self.canvas.delete("all")
        self.canvas = tk.Canvas(self.frame,width=675,height=350)
        self.canvas.grid(row=2, column=0,columnspan=2)
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=2, column=3, sticky="ns")
        scrollbar2 = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        scrollbar2.grid(row=15, column=0,columnspan=9, sticky="ew")
        self.inner_frame = tk.Frame(self.canvas,height=160)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        
        
    def on_rating_click(self):
        self.on_click()
        self.sort_by_rating_desc()
        
    def on_session_click(self):
        self.on_click()
        self.sort_by_session()
        
    def on_time_click(self):
        self.on_click()
        self.sort_by_time()
        
    def on_age_click(self):
        self.on_click()
        self.sort_by_age()
        
    def on_sex_click(self):
        self.on_click()
        self.sort_by_sex()
        
    def go_to_home(self):
        subprocess.Popen(["python", "op_home_page.py", O_id])  
        self.destroy()
            

if __name__=="__main__":
    O_id = sys.argv[1]
    if O_id is not None:
      O_id = str(O_id)
    #O_id="1"
    app=MHPReview(O_id)
    app.mainloop()
    


