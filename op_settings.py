import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import sys
import mysql.connector
import parkin_credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
class MHPSettings(tk.Tk):
    def __init__(self, O_id):
        super().__init__()
        self.title("Parkin - Operator Settings Page")
        self.geometry("900x600")
        #self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        #background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        #self.eval('tk::PlaceWindow . center')
        self.header_label = tk.Label(self, text="Settings Page", font=("Verdana", 14))
        self.header_label.place(relx=0.5, rely=0.01, anchor="n")
        
        self.back_button = tk.Button(self, text="<- Back", font=("Verdana", 10),command=self.go_to_home)
        self.back_button.place(relx=0.1, rely=0.01, anchor="n")

        self.frame1 = tk.Frame(self, bg="white", bd=4)
        self.frame1.place(relx=0.35, rely=0.1, relwidth=0.4, relheight=0.65)
        
        
        self.header_label = tk.Label(self, text="Settings Page", font=("Verdana", 14))
        self.header_label.place(relx=0.5, rely=0.01, anchor="n")
        
        self.back_button = tk.Button(self, text="<- Back", font=("Verdana", 10),command=self.go_to_home)
        self.back_button.place(relx=0.1, rely=0.01, anchor="n")

        self.frame1 = tk.Frame(self, bg="white", bd=4)
        self.frame1.place(relx=0.35, rely=0.1, relwidth=0.4, relheight=0.65)

        self.label1 = tk.Label(self.frame1, text="Edit your Details", bg="white", anchor="w", font=("Verdana", 12))
        self.label1.grid(row=0, column=0, padx=5, pady=5, columnspan=3, sticky="nw")

        # CREATE LABELS AND ENTRY FIELDS
        self.operatorname_label = tk.Label(self.frame1, text="Operator Name:", font=("Verdana", 10), bg="white")
        self.operatorname_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.operatorname_entry = tk.Entry(self.frame1, font=("Verdana", 10))
        self.operatorname_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.password_label = tk.Label(self.frame1, text="Password:", font=("Verdana", 10), bg="white")
        self.password_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = tk.Entry(self.frame1, font=("Verdana", 10), show="*")  # Use show="*" to hide the password
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.phone_label = tk.Label(self.frame1, text="Phone:", font=("Verdana", 10), bg="white")
        self.phone_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.phone_entry = tk.Entry(self.frame1, font=("Verdana", 10))
        self.phone_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.email_label = tk.Label(self.frame1, text="Email:", font=("Verdana", 10), bg="white")
        self.email_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = tk.Entry(self.frame1, font=("Verdana", 10))
        self.email_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.location_label = tk.Label(self.frame1, text="Location:", font=("Verdana", 10), bg="white")
        self.location_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.location_entry = tk.Entry(self.frame1, font=("Verdana", 10))
        self.location_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.floors_label = tk.Label(self.frame1, text="Floors:", font=("Verdana", 10), bg="white")
        self.floors_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.floors_entry = tk.Entry(self.frame1, font=("Verdana", 10))
        self.floors_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        self.slot_per_floor_label = tk.Label(self.frame1, text="Slots per Floor:", font=("Verdana", 10), bg="white")
        self.slot_per_floor_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.slot_per_floor_entry = tk.Entry(self.frame1, font=("Verdana", 10))
        self.slot_per_floor_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        self.rate_per_hour_label = tk.Label(self.frame1, text="Rate per Hour:", font=("Verdana", 10), bg="white")
        self.rate_per_hour_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.rate_per_hour_entry = tk.Entry(self.frame1, font=("Verdana", 10))
        self.rate_per_hour_entry.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        
        #POPULATE FIELDS WITH EXISTING DATA
        self.populate_data()
        
        #UPDATE BUTTON
        self.update_button = tk.Button(self.frame1, text="Update Details",width=25, font=("Verdana", 10), command=self.update_details)
        self.update_button.grid(row=9, column=0, columnspan=2,padx=5,pady=10,sticky="w")
        
        #DELETE BUTTON
        self.delete_button = tk.Button(self.frame1, text="Delete Account", width=25, font=("Verdana", 10), command=self.confirm_delete)
        self.delete_button.grid(row=10, column=0, columnspan=2,padx=5, pady=20,sticky="w")
    
    def populate_data(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query = "SELECT Operatorname, Password, Phone, Email, location, floors, slot_per_floor, Rate_per_hour FROM Operator WHERE O_id = %s"
        cur.execute(query, (str(O_id),))
        result = cur.fetchone()
        connection.close()

        if result:
            operatorname, password, phone, email, location, floors, slot_per_floor, rate_per_hour = result
            self.operatorname_entry.insert(0, operatorname)
            self.password_entry.insert(0, password)
            self.phone_entry.insert(0, phone)
            self.email_entry.insert(0, email)
            self.location_entry.insert(0, location)
            self.floors_entry.insert(0, floors)
            self.slot_per_floor_entry.insert(0, slot_per_floor)
            self.rate_per_hour_entry.insert(0, rate_per_hour)
        
    def update_details(self):
        operatorname = self.operatorname_entry.get()
        password = self.password_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        location = self.location_entry.get()
        floors = self.floors_entry.get()
        slot_per_floor = self.slot_per_floor_entry.get()
        rate_per_hour = self.rate_per_hour_entry.get()
    
        # Retrieve the current values from the database for comparison
        current_values = self.get_current_values()
    
        # Check if the values are the same as before updating
        if (floors, slot_per_floor) == current_values:
            messagebox.showinfo("No Changes", "No changes to update.")
            return
    
        # Update the details in the database
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query = "UPDATE Operator SET Operatorname = %s, Password = %s, Phone = %s, Email = %s, location = %s, floors = %s, slot_per_floor = %s, Rate_per_hour = %s WHERE O_id = %s"
        cur.execute(query, (operatorname, password, phone, email, location, floors, slot_per_floor, rate_per_hour, str(O_id)))
        connection.commit()
        connection.close()
    
        # Call the function to reset_slot_management if floors or slot_per_floor are being updated
        if floors or slot_per_floor:
            self.reset_slot_management()
    
        messagebox.showinfo("Success", "Details updated successfully!")
    

    def get_current_values(self):
        # Retrieve current values from the database
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query = "SELECT floors, slot_per_floor FROM Operator WHERE O_id = %s"
        cur.execute(query, (str(O_id),))
        result = cur.fetchone()
        connection.close()
    
        # Return the current values as a tuple
        return result if result else (None, None)

    def reset_slot_management(self):
        confirm_reset = messagebox.askyesno("Confirm Reset", "Are you sure you want to change your Parking Lot layout?\nThis action will delete existing slot occupancy data.")
        
        if not confirm_reset:
            
            return  # Do nothing if the user cancels the reset

        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query = "SELECT floors, slot_per_floor FROM Operator WHERE O_id = %s"
        cur.execute(query, (str(O_id),))
        result=cur.fetchone()
        floors=result[0]
        slots=result[1]
        
        #DELETE EXISTING VALUES IN TABLE
        query = "DELETE FROM Slot_Management WHERE O_id=%s"
        cur.execute(query, (str(O_id),))
        connection.commit()
        
        #INSERT INTO TABLE
        for i in range(1,int(floors)+1):
            for j in range (1,int(slots)+1):
                query= "INSERT INTO Slot_Management (O_id, Floor_no, Slot_no, Occupancy) VALUES (%s, %s, %s, 0)"
                cur.execute(query, (O_id, i, j))
                connection.commit() 
        print("Resetting slot_management...")
        
    
    def confirm_delete(self):
        result = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete your account?\nThis action is irreversible.")
        if result:
            self.delete_account()
        else:
            messagebox.showinfo("Account Deletion Canceled", "Your account was not deleted.")

        
    def delete_account(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        try:

            cur.execute("START TRANSACTION;")
            connection.commit()

            query = "DELETE FROM Feedback WHERE O_id = %s;"
            cur.execute(query, (O_id,))
            connection.commit()
           
            query = "DELETE FROM Payment WHERE Booking_id IN (SELECT Booking_id FROM Booking WHERE O_id=%s);"
            cur.execute(query, (O_id,))
            connection.commit()

            query = "DELETE FROM Reminder WHERE Booking_id IN (SELECT Booking_id FROM Booking WHERE O_id=%s)"
            cur.execute(query, (O_id,))
            connection.commit()           

            query = "DELETE FROM Booking WHERE O_id = %s;"
            cur.execute(query, (O_id,))
            connection.commit()
            
            query = "DELETE FROM Slot_management WHERE O_id=%s;"
            cur.execute(query, (O_id,))
            connection.commit()
            
            query = " DELETE FROM Operator WHERE O_id = %s;"
            cur.execute(query, (O_id,))
            connection.commit()
            

            cur.execute("COMMIT;")
            connection.commit()

            cur.execute("ROLLBACK;")
            connection.commit()

            connection.commit()
            connection.close()
            self.destroy()

        except Exception as e:
            connection.rollback()
            print("Error:", str(e))
        #except mysql.connector.Error as e:
            #connection.rollback()
            #print(f"Error: {e}")
            print(e)
        finally:
            connection.close()
            messagebox.showinfo("Account Deleted", "Your account has been deleted.")
            
    def go_to_home(self):
            subprocess.Popen(["python", "op_home_page.py", O_id])  
            self.destroy()
            

if __name__=="__main__":
    #M_id = sys.argv[1]
    #if M_id is not None:
    #  M_id = str(M_id)
    O_id="1"
    app=MHPSettings(O_id)
    app.mainloop()
    

        


