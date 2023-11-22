import tkinter as tk
import subprocess
import sys
import mysql.connector
import datetime
from tkinter import messagebox
import inspect
import parkin_credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
#from PIL import Image, ImageTk

class opHomePage(tk.Tk):
    def __init__(self,O_id):
        super().__init__()
        self.title("Parkin-Operator Home Page!")
        self.geometry("900x600")
        #self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        #background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        
        self.header_label = tk.Label(self, text="Home Page", font=("Verdana", 16))
        self.header_label.place(relx=0.5, rely=0.01, anchor="n",)
        
        #SETTINGS BUTTON
        self.settings_button = tk.Button(self, text="Settings", font=("Verdana", 12),command=self.go_to_settings)
        self.settings_button.place(relx=0.9, rely=0.01, anchor="n")

        #FRAME FOR UPCOMING APPOINTMENTS
        self.frame1 = tk.Frame(self, bg="white", bd=4)
        self.frame1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.75)
        
        #USE TO DISPLAY FLOOR NUMBER.
        #self.label1 = tk.Label(self.frame1, text="Dashboard", bg="white", anchor="w", font=("Verdana", 10))
        #self.label1.grid(row=0, column=0, padx=5, pady=5, columnspan=3,sticky="nw")
        
        #CANVAS FOR UPCOMING REQUESTS
        self.canvas = tk.Canvas(self.frame1,width=660,height=380)
        self.canvas.grid(row=1, column=0,columnspan=4)

        
        #FRAME FOR VIEWING APPOINTMENTS, SCHEDULE AND REVIEWS
        self.frame3 = tk.Frame(self, bg="white", bd=4)
        self.frame3.place(relx=0.1, rely=0.84, relwidth=0.8, relheight=0.1)
        
        self.payment_button = tk.Button(self.frame3, text="Manage Payment", font=("Verdana", 12),command=self.payment_manage)
        self.payment_button.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        
        self.feedback_button = tk.Button(self.frame3, text="View Feedbacks", font=("Verdana", 12),command=self.feedbacks)
        self.feedback_button.grid(row=0, column=2, padx=(50,20), pady=5, sticky="e")
        self.viewslots()
        
    
    def viewslots(self):
            connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            query= "SELECT floors,slot_per_floor FROM Operator WHERE O_id = %s"
            cur.execute(query, (str(O_id),))
            result = cur.fetchone()
            floors=result[0]
            slot_per_floor=result[1]
            
            query="SELECT floor_no,slot_no,Occupancy,U_id FROM Slot_Management WHERE O_id=%s"
            cur.execute(query, (str(O_id),))
            result = cur.fetchall()
            print(result)
            connection.close()
            
            self.data=result
            # Determine the maximum floor number
            self.max_floor = max(item[0] for item in self.data)

            # Set the initial floor
            self.current_floor = 1

            #num_rows = create_grid(root, data, current_floor, slots_per_row)
            
            # Create the grid for the initial floor
            self.create_grid(self.canvas, self.data, self.current_floor)
            

            # Create "Next" and "Back" buttons
            next_button = tk.Button(self.canvas, text="Next", command=self.next_floor)
            next_button.grid(row=2, column=0, pady=10)

            prev_button = tk.Button(self.canvas, text="Back", command=self.prev_floor)
            prev_button.grid(row=2, column=1, pady=10)

            # Create a label to display the current floor
            floor_label = tk.Label(self.canvas, text=f"Floor: {self.current_floor}")
            floor_label.grid(row=2, column=2, pady=10)
            
            """
            next_button = tk.Button(self.canvas, text="Next", command=self.next_floor)
            next_button.grid(row=num_rows, column=0, pady=10)

            prev_button = tk.Button(self.canvas, text="Back", command=self.prev_floor)
            prev_button.grid(row=num_rows, column=1, pady=10)

            # Create a label to display the current floor
            floor_label = tk.Label(self.canvas, text=f"Floor: {self.current_floor}")
            floor_label.grid(row=num_rows, column=2, pady=10)
            """


            
    def create_grid(self, canvas, data, current_floor):
        for floor, slot_id, occupancy, _ in data:
            if floor == self.current_floor:
                # Create a label for each slot on the current floor
                label = tk.Label(canvas, text=slot_id, width=4, height=2, relief="solid")
    
                # Set background color based on occupancy
                if occupancy == 1:
                    label.config(bg="red", cursor="hand2")
                    # Bind the click event to the label
                    label.bind("<Button-1>", lambda event, f=floor, s=slot_id: self.on_slot_click(f, s))
                else:
                    label.config(bg="lightgreen")
    
                # Place the label in the grid
                label.grid(row=1, column=int(slot_id))


    def next_floor(self):
        
        #global current_floor
        if self.current_floor < self.max_floor:
            self.current_floor += 1
            self.update_grid()
            print(int(self.current_floor))
            self.update_floor_label()
            
    def prev_floor(self):
        #global current_floor
        if self.current_floor > 1:
            self.current_floor -= 1
            self.update_grid()
            self.update_floor_label()
        

    def update_floor_label(self):
            next_button = tk.Button(self.canvas, text="Next", command=self.next_floor)
            next_button.grid(row=2, column=0, pady=10)
        
            prev_button = tk.Button(self.canvas, text="Back", command=self.prev_floor)
            prev_button.grid(row=2, column=1, pady=10)
            self.floor_label = tk.Label(self.canvas, text=f"Floor: {self.current_floor}")
            self.floor_label.grid(row=2, column=2, pady=10)
            self.floor_label.config(text=f"Floor: {self.current_floor}")
        
    def update_grid(self):
            # Destroy the current grid  
            for widget in self.canvas.winfo_children():
                widget.destroy()
        
            # Create the grid for the new floor
            self.create_grid(self.canvas, self.data, self.current_floor)
        
            # Update the floor label if it exists
            #if self.floor_label.winfo_exists():
            self.update_floor_label()
                
    def on_slot_click(self,floor, slot_id):
        print(f"Slot clicked - Floor: {floor}, Slot ID: {slot_id}")
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query= "SELECT U_id FROM Slot_Management WHERE O_id = %s AND floor_no=%s AND slot_no=%s"
        cur.execute(query, (str(O_id),floor,slot_id))
        U_id = str(cur.fetchone()[0])
        subprocess.Popen(["python", "op_booked_details.py", O_id, U_id])  
        self.destroy()
        
    
    def feedbacks(self):
        subprocess.Popen(["python", "op_feedback.py", O_id])  
        self.destroy()
    
    def payment_manage(self):
        subprocess.Popen(["python", "op_payment.py", O_id])  
        self.destroy()
        
    def go_to_settings(self):
        subprocess.Popen(["python", "op_settings.py", O_id])  
        self.destroy()
        
if __name__=="__main__":
    #M_id = sys.argv[1] if len(sys.argv) > 1 else None
    #if M_id is not None:
    #    M_id = str(M_id)
    O_id="1"
    app=opHomePage(O_id)
    app.mainloop()
    