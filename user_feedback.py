from tkinter import *
from tkinter import messagebox
import mysql.connector
from datetime import date

class FeedbackPage:
    def __init__(self, parent, user_id, operator_id):
        self.parent = parent
        self.user_id = user_id
        self.operator_id = operator_id

        self.window = Toplevel(self.parent)
        self.window.title("Feedback")
        self.window.geometry("400x300")
        self.window.config(bg="white")

        self.comment_label = Label(self.window, text="Your Feedback:")
        self.comment_label.pack()

        self.comment_entry = Entry(self.window, width=50)
        self.comment_entry.pack()

        self.submit_button = Button(self.window, text="Submit Feedback", command=self.submit_feedback)
        self.submit_button.pack()

    def submit_feedback(self):
        try:
            feedback_comment = self.comment_entry.get()
            today = date.today().isoformat()

            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='deepthi1600',
                database='PARKIN'
            )
            cursor = connection.cursor()

            query = "INSERT INTO Feedback (U_id, O_id, Comment, Date) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (self.user_id, self.operator_id, feedback_comment, today))
            connection.commit()

            messagebox.showinfo("Success", "Feedback submitted successfully")
            connection.close()
            self.window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error accessing database: {err}")

if __name__ == "__main__":
    # Replace user_id and operator_id with actual values when creating FeedbackPage object
    root = Tk()
    user_id = 1  # Replace with the user's ID
    operator_id = 1  # Replace with the operator's ID
    obj = FeedbackPage(root, user_id, operator_id)
    root.mainloop()
