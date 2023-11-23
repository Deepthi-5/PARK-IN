import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox
import parkin_credentials as cr
from tkcalendar import Calendar
#from practice import UserSettingsPage
from datetime import datetime
import datetime
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
import subprocess
import sys
class MyGUI:
    def __init__(self,U_NAME):
        root = tk.Tk()
        self.root = root
        self.username=U_NAME
        self.selected_time_slots = {}
        self.root.title("Operator Search")
        background = Label(self.root).place(x=0,y=0,relwidth=1,relheight=1)
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.selected_option = tk.StringVar()
        label = tk.Label(root, text="Select an option:", font=("times new roman", 12))
        label.place(x=100, y=100)
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cursor = connection.cursor()
        cursor.execute("SELECT u_id FROM user WHERE username = %s", (self.username,))
        result= cursor.fetchone()
        if result:
            self.userid = result[0]
        else:
            # Handle the case where no results were found for the username
            self.userid = None
        #print("uid in s.py is",self.userid)
        connection.commit()
        cursor.close()
        connection.close()
        option_buttons = []
        options = ["Name", "Availability","Highest Rating", "New Mall", "Maximum Reviews"]
        label = tk.Label(root, text="2.Select a button",font = ("Times New Roman", 12, "bold italic underline"))
        label.place(x=250, y=50)
        for i, option in enumerate(options):
            option_button = tk.Button(root, text=option, command=lambda opt=option: self.set_selected_option(opt))
            option_buttons.append(option_button)
            option_button.place(x=250 , y=100+ i*30)

        find_operator_button = tk.Button(root, text="Find Operator", command=self.find_operator)
        find_operator_button.place(x=100, y=150)
        label = tk.Label(root, text="3.Apply Selected Options",font = ("Times New Roman", 12, "bold italic underline"))
        label.place(x=50, y=125)
        label = tk.Label(root, text="Find Operator",font = ("Times New Roman", 12, "bold italic underline"))
        label.place(x=600, y=50)
        #font=("times new roman", 12)

        # Create an empty Treeview widget initially (hidden)
        self.tree = ttk.Treeview(root, columns=("OperatorName", "Phone", "Email", "Location", "slot_per_floor","Rate_per_hour"))
        self.tree.heading("#1", text="Operator Name")
        self.tree.heading("#2", text="Phone")
        self.tree.heading("#3", text="Email")
        self.tree.heading("#4", text="Location")
        self.tree.heading("#5", text="Slots per Floor")
        self.tree.heading("#6", text="Rate per Hour")
        self.tree.column("#1", width=100)
        self.tree.column("#2", width=100)
        self.tree.column("#3", width=50)
        self.tree.column("#4", width=100)
        self.tree.column("#5", width=200)
        self.tree.column("#6", width=200)
        #self.tree.place(x=200,y=200)
        self.tree.tag_configure("button", foreground="blue")
        self.tree.tag_bind("button", "<Button-1>", self.show_schedule)
        self.username=U_NAME
        # settings_button = tk.Button(root, text="Settings", command=self.redirect)
        # settings_button.place(x=700, y=10) 
        self.date_dropdown = tk.StringVar()
        self.date_dropdown.set("Select Date")
        self.date_dropdown_menu = ttk.Combobox(root, textvariable=self.date_dropdown)
        self.date_dropdown_menu.place(x=100, y=100)
        label = tk.Label(root, text="1.Select A Date",font = ("Times New Roman", 12, "bold italic underline"))
        label.place(x=100, y=50)

        # Calculate the next 5 days
        today = datetime.date.today()
        print("todays date",today)
        next_5_days = [today + datetime.timedelta(days=i-1) if (today + datetime.timedelta(days=i)).strftime('%A') in ["Saturday", "Sunday"] else today + datetime.timedelta(days=i) for i in range(1, 6)]
        formatted_dates = [date.strftime("%Y/%m/%d") for date in next_5_days]
        self.date_dropdown_menu['values'] = formatted_dates
        root.mainloop()
    def set_selected_option(self, option):
        selected_option = self.selected_option.get()
        self.selected_option.set(option)
        """if selected_option == "Speciality":
            self.text_entry1.destroy()  # Remove the "Enter Speciality" entry box
            self.label1.destroy()"""
        if option=="Name":
            self.label = tk.Label(self.root, text="Enter First Name")
            self.label.place(x=250, y=50)
            self.text_entry = tk.Entry(self.root)
            self.text_entry.place(x=350, y=100)
        elif option=="Speciality":
            self.label1 = tk.Label(self.root, text="Enter Speciality(trauma informed(T), child specialist(C) ,disability friendly(D) ,Queer friendly(Q))")
            self.label1.place(x=250, y=50)
            self.text_entry1 = tk.Entry(self.root)
            self.text_entry1.place(x=350, y=100)
        
    def find_operator(self):
        selected_option = self.selected_option.get()
        if selected_option=="Name":
            user_input = self.text_entry.get()
            self.text_entry.destroy()  # Remove the "Enter Speciality" entry box
            self.label.destroy()
            if user_input=="":
             messagebox.showerror("Please enter valid details", parent=self.root)
             return
        


        """if user_input == "" or (selected_option!="Highest Rating" and selected_option!="New Doctor" and selected_option!="Highest Rating in Trauma_Informed" and selected_option!="Maximum Reviews"):
            messagebox.showerror("Please enter valid details", parent=self.root)
            return"""

        try:
            connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            query = ""

            if selected_option == "Name":
                query = "SELECT Operatorname, phone, email, location, slot_per_floor,rate_per_hour FROM operator WHERE Operatorname = %s"
                cur.execute(query, (user_input,))

            elif selected_option == "Experience":
                query = "SELECT first_name, last_name, age, experience, qualification FROM mhp order by experience"
                cur.execute(query)
            elif selected_option == "Highest Rating":
                query = """SELECT m.first_name, m.last_name, m.age, m.experience, m.qualification
                FROM mhp m
                JOIN (
                    SELECT m_id, Rating
                    FROM Review
                    WHERE Rating = (
                        SELECT MAX(Rating)
                        FROM Review
                    )
                ) max_rated_doctors
                ON m.m_id = max_rated_doctors.m_id;"""
                #print("executed query")
                #cur.execute(query, (user_input,))
                cur.execute(query)
            elif selected_option == "New Doctor":
                query = "SELECT first_name, last_name, age, experience, qualification FROM mhp where m_id NOT IN (SELECT m_id FROM Review)"
                cur.execute(query)
            elif selected_option == "Maximum Reviews":
                query = """SELECT D.First_Name, D.Last_Name, D.Age, D.Experience, D.Qualification
                    FROM mhp D
                    WHERE D.M_ID = (
                        SELECT Subquery.DoctorID
                        FROM (
                            SELECT D.M_ID AS DoctorID, COUNT(*) AS ReviewCount
                            FROM Review R
                            JOIN mhp D ON R.M_ID = D.M_ID
                            GROUP BY DoctorID
                            ORDER BY ReviewCount DESC
                            LIMIT 1
                        ) AS Subquery
                    );

                    """
                cur.execute(query)
           

            elif selected_option == "Age":
                query = "SELECT first_name, last_name, age, experience, qualification FROM mhp order by age"
                #print(user_input)
                #cur.callproc("SearchDoctorsByAge", (user_input,))
                cur.execute(query)
            elif selected_option == "Sex":
                query = "SELECT first_name, last_name, age, experience, qualification ,sex FROM mhp order by sex"
                #print(user_input)
                #cur.callproc("SearchDoctorsByAge", (user_input,))
                cur.execute(query)

           
            else:
                messagebox.showerror("Invalid Option", "Please select a valid option", parent=self.root)
                return

            #cur.execute(query, (user_input,))
            rows = cur.fetchall()
            print("rows",rows)

            if rows:
                # Clear previous entries in the Treeview
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Insert retrieved data into the Treeview
                # Inside your find_doctor function
                for row in rows:
                    item_id = self.tree.insert("", "end", values=row)
                    self.tree.item(item_id, tags=("button",))  # Apply the "button" tag

                # Bind the click event outside the loop
                self.tree.bind("<Button-1>", self.handle_tree_click)
                #self.tree.pack(padx=100, pady=200)
                self.tree.place(x=400,y=200)

            else:
                messagebox.showinfo("Operator Not Found", "No operator found for the provided details", parent=self.root)

        except Exception as e:
            print(e)





    # def redirect(self):
    #     print("s.py inside redirect uname",self.username)
    #     subprocess.Popen(["python3","/Users/tulasirambommisetty/Downloads/practice.py",self.username])

    def show_schedule(self, item_id):
        # Check if the selected item_id exists in the Treeview
        if self.tree.exists(item_id):
            # Get the selected doctor's data from the Treeview
            selected_operator_data = self.tree.item(item_id, "values")
            if selected_operator_data:
                operator_name = selected_operator_data[0]
                print("operator_name",operator_name)
                try:
                    connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                    cur = connection.cursor()

                    # Query to fetch the M_ID based on the doctor's name
                    o_id_query = "SELECT O_ID FROM operator WHERE Operatorname = %s"
                    cur.execute(o_id_query, (operator_name,))
                    o_id = cur.fetchone()

                    if o_id:
                        o_id = o_id[0] 
                        self.o_id=o_id
                        #print("m_id is",m_id)
                        # Create a new window for displaying the schedule
                        selected_date = self.date_dropdown.get()
                        print("selcted date is",selected_date)
                        if selected_date=="Select Date":
                            messagebox.showinfo("No Date Selected", "Select a Date", parent=self.root)
                        else:
                            # Establish connection to the database
                            connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                            cursor = connection.cursor()

                            # Find the next available slot for the selected operator and floor where Occupancy is 0
                            find_slot_query = """
                                SELECT Floor_no, Slot_no
                                FROM Slot_management
                                WHERE O_id = %s AND Occupancy = 0
                                ORDER BY Floor_no, Slot_no
                                LIMIT 1
                            """
                            cursor.execute(find_slot_query, (o_id,))
                            next_available_slot = cursor.fetchone()
                            print("nas",next_available_slot)
                            if next_available_slot:
                                booked_floor, slot_to_book = next_available_slot

                                # Update Slot_management table: Change Occupancy from 0 to 1 for the booked slot
                                update_slot_query = """
                                    UPDATE Slot_management
                                    SET Occupancy = 1
                                    WHERE O_id = %s AND Floor_no = %s AND Slot_no = %s
                                """
                                cursor.execute(update_slot_query, (o_id, booked_floor, slot_to_book))
                                connection.commit()

                                # Insert booking record into Booking table
                                current_date = datetime.now().date()
                                current_time = datetime.now().time()

                                insert_booking_query = """
                                    INSERT INTO Booking (Booking_id,U_id, O_id, Floor_no, Slot_no, Date, Time)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                """
                                cursor.execute(insert_booking_query, (self.user_id, o_id, booked_floor, slot_to_book, current_date, current_time))
                                connection.commit()
                                
                                # Display a message to inform successful booking
                                messagebox.showinfo("Booking Successful", f"Slot {slot_to_book} on Floor {booked_floor} has been booked.", parent=self.root)
                            else:
                                # If no available slots found, display a message
                                messagebox.showinfo("No Available Slot", "No available slots for booking.", parent=self.root)

                            

                except Exception as e:
                    print(e)

   
    

        
    def create_book_appointment_button(self, doctor):
        # Create a "Book Appointment" button for the given doctor
        book_appointment_button = tk.Button(self.tree, text="Book Appointment", command=lambda doctor=doctor: self.show_schedule(doctor))
        self.tree.window_create(doctor, window=book_appointment_button)

    def open_settings(self):
        # Create an instance of your userSettings class
        try:
            settings_window = tk.Toplevel()
            #username = "chaitra08"
            settings_window.title("User Settings")
            settings = UserSettingsPage(settings_window,U_NAME)
        except Exception as e:
            print(f"Error opening settings: {e}")

    
    def handle_tree_click(self, event):
        item_id = self.tree.identify_row(event.y)  # Get the item ID that was clicked
        if self.tree.tag_has("button", item_id):
                #print(item_id)
                self.show_schedule(item_id)

    """def redirect_window(self):
        username=self.uname_txt.get()
        self.window.destroy()
        subprocess.Popen(["python","s.py"])"""

   

if __name__ == '__main__':
    """U_NAME=sys.argv[1]
    #print(U_NAME)
    if U_NAME is not None:
        U_NAME=str(U_NAME)"""
    U_NAME="chai08"
    #root = tk.Tk()
    #U_NAME="nirvan"
    app = MyGUI(U_NAME)
    #root.mainloop()
