import tkinter as tk
from tkinter.constants import RIGHT
from PIL import ImageTk, Image
import center_tk_window
from tkinter import Toplevel
import sqlite3
import tkinter.ttk as ttk

#CREATE MAIN WINDOW
root = tk.Tk()
root.title("Address Book")
root.configure(background="#F2F4F3")
root.geometry("400x400")
center_tk_window.center_on_screen(root)

#Place address book icon in the corner
root.iconbitmap('images\\icon.ico')

#CREATE IMAGES: (people logo), resize image, show image
image = Image.open("images\\people.png")
image = image.resize((170, 170), Image.ANTIALIAS)
people_image = ImageTk.PhotoImage(image)
people_image_label = tk.Label(image=people_image,bg="#F2F4F3")
people_image_label.place(x=200, y=150, anchor=tk.CENTER)

#CREATE LABELS: start greeting, show label
greeting_label = tk.Label(root, text="Welcome to your Address book!\n Click start",fg="#0A0908", bg="#F2F4F3")
greeting_label.place(x=200, y=270, anchor=tk.CENTER)

#CREATE A DB AND CONNECTION
connection = sqlite3.connect('address_book.db')
cursor = connection.cursor()

#CREATE DATABASE TABLE *create only once 
# cursor.execute("""CREATE TABLE contact (
#                      First_name text,
#                      Last_name text,
#                      Address text,
#                      Phone_number integer,
#                      Email text
#                  )
#                 """)


#Create main menu
def start():
    """Function to display main menu in root window"""
        
    #Clear window from greeting labels and buttons
    greeting_label.destroy()
    start_button.destroy()
    exit_button.destroy()
    
    #Create labels
    menu_message_label = tk.Label(root, text="Choose an option",fg="#0A0908", bg="#F2F4F3")
    #Display
    menu_message_label.place(x=200, y=250, anchor=tk.CENTER)
    
    #Create and 5 buttons, (add, view, search, edit, delete, exit)
    menu_add_contact_button = tk.Button(root, text="Add Contact", command=add_contact,  bg="#5E503F", fg="#F2F4F3", height=1, width=13)
    menu_view_contacts_button = tk.Button(root, text="View Contacts", command=view_contacts, bg="#5E503F", fg="#F2F4F3", height=1, width=13)
    menu_edit_contact_button = tk.Button(root, text="Edit Contact", command=edit_contact, bg="#5E503F", fg="#F2F4F3", height=1, width=13)
    menu_search_contact_button = tk.Button(root, text="Search Contact", command=search_contact, bg="#5E503F", fg="#F2F4F3", height=1, width=13)
    menu_delete_contact_button = tk.Button(root, text="Delete Contact", command=delete_contact, bg="#5E503F", fg="#F2F4F3", height=1, width=13)
    menu_exit_button = tk.Button(root, text="Exit", command=root.quit, bg="#5E503F", fg="#F2F4F3", height=1, width=13)
    #Display
    menu_add_contact_button.place(x=80, y=300, anchor=tk.CENTER)
    menu_view_contacts_button.place(x=200, y=300, anchor=tk.CENTER)
    menu_edit_contact_button.place(x=320, y=300, anchor=tk.CENTER)
    menu_search_contact_button.place(x=80, y=350, anchor=tk.CENTER)
    menu_delete_contact_button.place(x=200, y=350, anchor=tk.CENTER)
    menu_exit_button.place(x=320, y=350, anchor=tk.CENTER)

def add_contact():
    """Function to add a new contact to DB. Read starting from under the "submit_new_sql" function"""

    def submit_new_sql():
        """Funtion to execute adding contact to DB using SQL command. Execution on clicked 'submit_button'"""
            
        #Connect
        connection = sqlite3.connect('address_book.db')
        cursor = connection.cursor()
        
        records_number = None
        records_email= None
        
        #Loop through existing contacts to find if phone number or email already exists
        valid = True
        
            #Select all from contacts where the phone number is the same as entered one
            #Fetching one row is enough to have a match and to return a error label
        if phone_entry.get() == 0:
            valid = False
            error_label = tk.Label(window, text="Number cannot be zero!",fg="#0A0908", bg="#F2F4F3")
            error_label.grid(row=15, column=0, columnspan=2)
            valid = False
            error_label.after(5000, error_label.destroy)
            
        cursor.execute("""SELECT * FROM contact WHERE Phone_number = ? and  Phone_number not like ?""",(phone_entry.get(),0,))
        records_number = cursor.fetchone()
        if records_number == None:
            pass
        else:
            error_label = tk.Label(window, text="A contact already has that phone number!",fg="#0A0908", bg="#F2F4F3")
            error_label.grid(row=8, column=0, columnspan=2)
            valid = False
            error_label.after(5000, error_label.destroy)
            
            #Select all from contacts where email is the same as entered one
            #Fetching one row is enough to match and to return a error label
        cursor.execute("""SELECT *, oid FROM contact WHERE Email = ?""",(email_entry.get(),))
        records_email = cursor.fetchone()
        if records_email == None:
            pass
        else:
            error_label = tk.Label(window, text="A contact already has that email!",fg="#0A0908", bg="#F2F4F3")
            error_label.grid(row=9, column=0, columnspan=2)
            valid = False
            error_label.after(5000, error_label.destroy)
        
        #If no errors are found, add contact to tabel
        if valid == True:   
            
            #Execute 
            cursor.execute("""INSERT INTO contact (First_name, Last_name, Address, Phone_number, Email)
                        VALUES (?, ?, ?, ?, ?)""",
                        (fname_entry.get(),lname_entry.get(),address_entry.get(),phone_entry.get(),email_entry.get()))
                
            #Submit and close connection
            connection.commit()
            connection.close()
                
            #Create success message
            success_label = tk.Label(window, text="Contact addedd!",fg="#0A0908", bg="#F2F4F3")
            #Display
            success_label.grid(row=10, column=0, columnspan=2)
            success_label.after(5000, success_label.destroy)
                
            #Clear all entries
            fname_entry.delete(0,tk.END)
            lname_entry.delete(0,tk.END)
            address_entry.delete(0,tk.END)
            phone_entry.delete(0,tk.END)
            email_entry.delete(0,tk.END)
    
    #Create new window
    window = Toplevel()
    window.title("Add new contact")
    window.iconbitmap('images\\icon.ico')
    window.geometry("400x400")
    window.configure(background="#F2F4F3")
    
    #Create labels for entries
    message_label = tk.Label(window,  text="Enter fields", pady=10)
    fname_label = tk.Label(window, text="First Name: ")
    lname_label = tk.Label(window, text="Last Name: ")
    address_label = tk.Label(window, text="Address: ")
    phone_label = tk.Label(window, text="Phone Number: ")
    email_label = tk.Label(window, text="Email: ")
    #Display
    message_label.grid(row=0, column=0, columnspan=2)
    fname_label.grid(row=1, column=0, pady=2)
    lname_label.grid(row=2, column=0, pady=2)
    address_label.grid(row=3, column=0, pady=2)
    phone_label.grid(row=4, column=0, pady=2)
    email_label.grid(row=5, column=0, pady=2)
    
    #Create entrys
    fname_entry = tk.Entry(window, width=35, border= 5)
    lname_entry = tk.Entry(window, width=35, border= 5)
    address_entry = tk.Entry(window, width=35, border= 5)
    phone_entry = tk.Entry(window, width=35, border= 5)
    email_entry = tk.Entry(window, width=35, border= 5)
    #Display
    fname_entry.grid(row=1, column=1, pady=2)
    lname_entry.grid(row=2, column=1, pady=2)
    address_entry.grid(row=3, column=1, pady=2)
    phone_entry.grid(row=4, column=1, pady=2)
    email_entry.grid(row=5, column=1, pady=2)

    #Create button: submit_new_sql
    submit_button = tk.Button(window, text="Add", command=submit_new_sql, bg="#5E503F", fg="#F2F4F3",  height = 1, width = 13)
    submit_button.grid(row=6, column=0, columnspan=2)
    
def view_contacts():
    """Function to preview all contacts in DB"""
    
    #Create new window
    window = Toplevel()
    window.title("View all contacts")
    window.iconbitmap('images\\icon.ico')
    window.geometry("800x400")
    window.configure(background="#F2F4F3")
    
    #Create label
    message_label = tk.Label(window, text="YOUR CONTACTS",fg="#0A0908", bg="#F2F4F3")
    #Display
    message_label.place(x=400, y=50, anchor=tk.CENTER)
    
    #Connect
    connection = sqlite3.connect('address_book.db')
    cursor = connection.cursor()
        
    #Execute query
    cursor.execute("""SELECT *, oid FROM contact""")
    records = cursor.fetchall()
        
    #Create frame to place tabel(treeview) and scrollbar   
    frame = tk.Frame(window)
    
    #Create scrollbar and place it in frame
    scrollbar = tk.Scrollbar(frame)
    
    #Crate table using treeview and place it in frame
    tree = ttk.Treeview(frame, selectmode="browse", yscrollcommand=scrollbar.set)
        
    #Set scrollbar command to view tabel vertically
    scrollbar.config(command=tree.yview)
        
    #Define table: columns (like in DB)
    tree['columns'] = ("First Name","Last Name","Address","Phone Number","Email","oid")
        
    #Format columns, #0 is the column that treeview adds alone
    tree.column("#0", width=0)
    tree.column("First Name",anchor=tk.W, width=100)
    tree.column("Last Name", anchor=tk.W, width=100)
    tree.column("Address", anchor=tk.W, width=150)
    tree.column("Phone Number", anchor=tk.W, width=100)
    tree.column("Email", anchor=tk.W, width=200)
    tree.column("oid", anchor=tk.W, width=30)
        
    #Format Headings (header row)
    tree.heading("#0", text="",anchor=tk.CENTER)
    tree.heading("First Name", text="First Name",anchor=tk.CENTER)
    tree.heading("Last Name", text="Last Name",anchor=tk.CENTER)
    tree.heading("Address", text="Address",anchor=tk.CENTER)
    tree.heading("Phone Number", text="Phone Number",anchor=tk.CENTER)
    tree.heading("Email", text="Email",anchor=tk.CENTER)
    tree.heading("oid", text="ID",anchor=tk.CENTER)
        
    #Inserting data into rows from records (cursor.fetchall()), set counter "i" to add to specific row
    i=0
    for record in records:
        tree.insert(parent='', index='end', iid=i, values=record)
        i+=1
    
    #Display frame, place scrollbar and tree
    frame.pack(pady=20)
    scrollbar.pack(side=RIGHT, fill=tk.Y)
    tree.pack()
        
    #Submit and close connection
    connection.commit()
    connection.close()

def edit_contact():
    """Function to edit a existing contact in DB """
    
    #Create new window
    window = Toplevel()
    window.title("Edit Contact")
    window.iconbitmap('images\\icon.ico')
    window.geometry("400x400")
    window.configure(background="#F2F4F3")
    
    #Create label
    message_label = tk.Label(window, text="Enter contact ID",fg="#0A0908", bg="#F2F4F3")
    message_label.place(x=200, y=200, anchor=tk.CENTER)
    
    #Create Entry for contact ID
    id_entry = tk.Entry(window, width=35, border= 5)
    id_entry.place(x=200, y=230, anchor = tk.CENTER)
    
    #Create labels
    message_label = tk.Label(window,  text="Edit fields", pady=10)
    fname_label = tk.Label(window, text="First Name: ")
    lname_label = tk.Label(window, text="Last Name: ")
    address_label = tk.Label(window, text="Address: ")
    phone_label = tk.Label(window, text="Phone Number: ")
    email_label = tk.Label(window, text="Email: ")
    #Display
    message_label.grid(row=0, column=0, columnspan=2)
    fname_label.grid(row=1, column=0, pady=2)
    lname_label.grid(row=2, column=0, pady=2)
    address_label.grid(row=3, column=0, pady=2)
    phone_label.grid(row=4, column=0, pady=2)
    email_label.grid(row=5, column=0, pady=2)
    
    #Create Entry for found contact (Here the found contact will be placed)
    fname_entry = tk.Entry(window, width=35, border= 5)
    lname_entry = tk.Entry(window, width=35, border= 5)
    address_entry = tk.Entry(window, width=35, border= 5)
    phone_entry = tk.Entry(window, width=35, border= 5)
    email_entry = tk.Entry(window, width=35, border= 5)
    #Display
    fname_entry.grid(row=1, column=1, pady=2)
    lname_entry.grid(row=2, column=1, pady=2)
    address_entry.grid(row=3, column=1, pady=2)
    phone_entry.grid(row=4, column=1, pady=2)
    email_entry.grid(row=5, column=1, pady=2)
    
    #Search by id
    def search_id():
        """Function to search DB for contact under entered ID. Execuction on "search_id_button" click"""
    
        #Try to look if entered id exists, if not return error label (error for not entering an id or for id not found)
        try:
            
            #Connect
            connection = sqlite3.connect('address_book.db')
            cursor = connection.cursor()
        
            #Execute query
            cursor.execute("SELECT * FROM contact WHERE oid= " + id_entry.get())
            record = cursor.fetchone()
            
            #Place found contact in entry boxes
            fname_entry.insert(0,record[0])
            lname_entry.insert(0,record[1])
            address_entry.insert(0,record[2])
            phone_entry.insert(0,record[3])
            email_entry.insert(0,record[4])
            
            #SQL 
            def update():
                """Function to update a contact, execution on "update_button" click"""
                
                #connect
                connection = sqlite3.connect('address_book.db')
                cursor = connection.cursor()
                
                records_number = None
                records_email= None
                #Loop through existing contacts to find if phone number or email already exists
                valid = True
                
                    #Search to see if updated entry is aleady in database, "entered id excluded so it wont look at the current changed contact"
                cursor.execute("""SELECT * FROM contact WHERE Phone_number = ? AND oid not like ?""",(phone_entry.get(),id_entry.get()))
                records_number = cursor.fetchone()
                if records_number == None:
                    pass
                else:
                    error_label = tk.Label(window, text="A contact already has that phone number!",fg="#0A0908", bg="#F2F4F3")
                    error_label.place(x=200, y=290, anchor=tk.CENTER)
                    valid = False
                    error_label.after(5000, error_label.destroy)
                    
                    #Search to see if updated entry is aleady in database, "entered id excluded so it wont look at the current changed contact"
                cursor.execute("""SELECT *, oid FROM contact WHERE Email = ? AND oid not like ? """,(email_entry.get(),id_entry.get()))
                records_email = cursor.fetchone()
                if records_email == None:
                    pass
                else:
                    error_label = tk.Label(window, text="A contact already has that email!",fg="#0A0908", bg="#F2F4F3")
                    error_label.place(x=200, y=290, anchor=tk.CENTER)
                    valid = False
                    error_label.after(4000, error_label.destroy)
                
                #If no errors are found, update contact
                if valid == True:   
                    #Execute
                    cursor.execute("UPDATE contact SET First_name=?, Last_name=?, Address=?, Phone_number=?,Email=? WHERE oid= " +id_entry.get(), 
                            (fname_entry.get(), lname_entry.get(), address_entry.get(),phone_entry.get(),email_entry.get()))

                    #Create success message label
                    message_label = tk.Label(window, text="Contact updated!",fg="#0A0908", bg="#F2F4F3")
                    message_label.place(x=200, y=290, anchor=tk.CENTER)
                    message_label.after(4000, message_label.destroy)
            
                #Submit and close connection
                connection.commit()
                connection.close() 
                
                #Remove contact fom entry display
                fname_entry.delete(0,tk.END)
                lname_entry.delete(0,tk.END)
                address_entry.delete(0,tk.END)
                phone_entry.delete(0,tk.END)
                email_entry.delete(0,tk.END)
                id_entry.delete(0,tk.END)
                update_id_button.destroy()
                
            #Create button
            update_id_button = tk.Button(window, text="Update", command=update, bg="#5E503F", fg="#F2F4F3",  height = 1, width = 13)
            update_id_button.place(x=200, y=260, anchor=tk.CENTER)

            #Submit and close connection
            connection.commit()
            connection.close() 
                
        except TypeError: 
            #Create success message label
            message_label = tk.Label(window, text="Contact not found!",fg="#0A0908", bg="#F2F4F3")
            message_label.place(x=200, y=290, anchor=tk.CENTER)
            message_label.after(3000, message_label.destroy)
        except sqlite3.OperationalError:
            message_label = tk.Label(window, text="Enter ID",fg="#0A0908", bg="#F2F4F3")
            message_label.place(x=200, y=300, anchor=tk.CENTER)
            message_label.after(3000, message_label.destroy)
            
    #Create button
    search_id_button = tk.Button(window, text="Search ", command=search_id, bg="#5E503F", fg="#F2F4F3",  height = 1, width = 13)
    search_id_button.place(x=200, y=260, anchor=tk.CENTER)

#Global elements for search_contact function
#Needed for being able to clear and add elements from screen if choice is changed
search_name_message_label = None
search_number_message_label = None
search_id_message_label= None
search_fname_label = None
search_lname_label = None
search_number_label = None
search_id_label = None
fname_entry = None
lname_entry = None
number_entry = None
id_entry = None
counter = None
def search_contact():
    """Function to search for a contact. 3 ways to search (by name, by number, by id)"""
    
    #Create new window
    window = Toplevel()
    window.title("Search Contact")
    window.iconbitmap('images\\icon.ico')
    window.geometry("800x500")
    window.configure(background="#F2F4F3")
    
    def by_name():
        """Function to place elements on screen and search for contact by name, execution on "by_name" button click"""

        global search_name_message_label 
        global search_number_message_label 
        global search_id_message_label
        global search_number_label
        global search_fname_label 
        global search_lname_label 
        global search_id_label
        global fname_entry
        global lname_entry 
        global number_entry
        global id_entry
        global counter

        #Clear elements from last search, depending on type of last search
        if counter== 2:
            search_number_message_label.destroy()
            search_number_label.destroy()
            number_entry.destroy()
        elif counter == 3:
            search_id_message_label.destroy()
            search_id_label.destroy()
            id_entry.destroy()
            
        counter = 1
        
        #Create Label
        search_name_message_label = tk.Label(window, text="Enter information: ",fg="#0A0908", bg="#F2F4F3")
        search_fname_label = tk.Label(window, text="First Name",fg="#0A0908", bg="#F2F4F3")
        search_lname_label = tk.Label(window, text="Last Name",fg="#0A0908", bg="#F2F4F3")
        #Display
        search_name_message_label.place(x=400, y=120, anchor=tk.CENTER)
        search_fname_label.place(x=250, y=150, anchor=tk.CENTER)
        search_lname_label.place(x=250, y=180, anchor=tk.CENTER)
        
        #Create entry
        fname_entry = tk.Entry(window, width=35, border= 5)
        lname_entry = tk.Entry(window, width=35, border= 5)
        #Display
        fname_entry.place(x=400, y=150, anchor=tk.CENTER)
        lname_entry.place(x=400, y=180, anchor=tk.CENTER)
        
        def search_name():
            """Function to search the DB using SQL. Execution on search_button" click."""
            
            try:
                #Connect
                connection = sqlite3.connect('address_book.db')
                cursor = connection.cursor()
                
                #Execute query
                cursor.execute("SELECT *,oid FROM contact WHERE First_name = ? AND Last_name = ?",(fname_entry.get(), lname_entry.get()))
                records = cursor.fetchall()
                        
                #Create frame to place tabel(treeview) and scrollbar   
                frame = tk.Frame(window)
                
                #Create scrollbar and place it in frame
                scrollbar = tk.Scrollbar(frame)
                
                #Crate table using treeview and place it in frame
                tree = ttk.Treeview(frame, selectmode="browse", yscrollcommand=scrollbar.set)
                    
                #Set scrollbar command to view tabel vertically
                scrollbar.config(command=tree.yview)
                    
                #Define table: columns (like in DB)
                tree['columns'] = ("First Name","Last Name","Address","Phone Number","Email","oid")
                    
                #Format columns, #0 is the column that treeview adds alone
                tree.column("#0", width=0)
                tree.column("First Name",anchor=tk.W, width=100)
                tree.column("Last Name", anchor=tk.W, width=100)
                tree.column("Address", anchor=tk.W, width=150)
                tree.column("Phone Number", anchor=tk.W, width=100)
                tree.column("Email", anchor=tk.W, width=200)
                tree.column("oid", anchor=tk.W, width=50)
                    
                #Format Headings (header row)
                tree.heading("#0", text="", anchor=tk.CENTER)
                tree.heading("First Name", text="First Name", anchor=tk.CENTER)
                tree.heading("Last Name", text="Last Name", anchor=tk.CENTER)
                tree.heading("Address", text="Address", anchor=tk.CENTER)
                tree.heading("Phone Number", text="Phone Number", anchor=tk.CENTER)
                tree.heading("Email", text="Email", anchor=tk.CENTER)
                tree.heading("oid", text="ID", anchor=tk.CENTER)
                    
                #Inserting data into rows from records (cursor.fetchall()), set counter "i" to add to specific row
                i=0
                for record in records:
                    tree.insert(parent='', index='end', iid=i, values=record)
                    i+=1
                
                #Display frame, place scrollbar and tree
                frame.place(x=60, y=250)
                scrollbar.pack(side=RIGHT, fill=tk.Y)
                tree.pack()
            
                #Submit and close connection
                connection.commit()
                connection.close()
                
            except sqlite3.OperationalError:
                error_label = tk.Label(window, text="Enter name!", fg="#0A0908", bg="#F2F4F3")
                error_label.place(x=400, y=250, anchor=tk.CENTER)
                error_label.after(2000,error_label.destroy())
            
        #Create search button
        search_button = tk.Button(window, text="Search", command=search_name, bg="#5E503F", fg="#F2F4F3",  height = 1, width = 13)
        search_button.place(x=400, y=210, anchor = tk.CENTER)
        
    def by_number():
        """Function to place elements on screen and search for contact by number, execution on "by_number" button click"""
        
        global search_name_message_label 
        global search_number_message_label
        global search_id_message_label
        global search_number_label
        global search_fname_label 
        global search_lname_label
        global search_id_label 
        global fname_entry
        global lname_entry 
        global number_entry
        global id_entry
        global counter 
        
        #Clear elelemts from last search
        if counter == 1:
            search_name_message_label.destroy()
            search_fname_label.destroy()
            search_lname_label.destroy()
            fname_entry.destroy()
            lname_entry.destroy()
        elif counter == 3:
            search_id_message_label.destroy()
            search_id_label.destroy()
            id_entry.destroy()
            
        counter = 2
            
        #Create labels
        search_number_message_label = tk.Label(window, text="Enter information: ",fg="#0A0908", bg="#F2F4F3")
        search_number_label = tk.Label(window, text="Number",fg="#0A0908", bg="#F2F4F3")
        #Display
        search_number_message_label.place(x=400, y=120, anchor=tk.CENTER)
        search_number_label.place(x=250, y=150, anchor=tk.CENTER)
        
        #Create entry
        number_entry = tk.Entry(window, width=35, border= 5)
        #Display
        number_entry.place(x=400, y=150, anchor=tk.CENTER)
    
        def search_number():
            """Function to search the DB using SQL. Execution on "search_button" click."""
               
            try:  
                #Connect
                connection = sqlite3.connect('address_book.db')
                cursor = connection.cursor()
                
                #Execute query
                cursor.execute("SELECT *, oid FROM contact WHERE Phone_number = " + number_entry.get())
                records = cursor.fetchall()
                
                #Create frame to place tabel(treeview) and scrollbar   
                frame = tk.Frame(window)
                
                #Create scrollbar and place it in frame
                scrollbar = tk.Scrollbar(frame)
                
                #Crate table using treeview and place it in frame
                tree = ttk.Treeview(frame, selectmode="browse", yscrollcommand=scrollbar.set)
                    
                #Set scrollbar command to view tabel vertically
                scrollbar.config(command=tree.yview)
                    
                #Define table: columns (like in DB)
                tree['columns'] = ("First Name","Last Name","Address","Phone Number","Email","oid")
                    
                #Format columns, #0 is the column that treeview adds alone
                tree.column("#0", width=0)
                tree.column("First Name",anchor=tk.W, width=100)
                tree.column("Last Name", anchor=tk.W, width=100)
                tree.column("Address", anchor=tk.W, width=150)
                tree.column("Phone Number", anchor=tk.W, width=100)
                tree.column("Email", anchor=tk.W, width=200)
                tree.column("oid", anchor=tk.W, width=50)
                    
                #Format Headings (header row)
                tree.heading("#0", text="", anchor=tk.CENTER)
                tree.heading("First Name", text="First Name", anchor=tk.CENTER)
                tree.heading("Last Name", text="Last Name", anchor=tk.CENTER)
                tree.heading("Address", text="Address", anchor=tk.CENTER)
                tree.heading("Phone Number", text="Phone Number", anchor=tk.CENTER)
                tree.heading("Email", text="Email", anchor=tk.CENTER)
                tree.heading("oid", text="ID", anchor=tk.CENTER)
                    
                #Inserting data into rows from records (cursor.fetchall()), set counter "i" to add to specific row
                i=0
                for record in records:
                    tree.insert(parent='', index='end', iid=i, values=record)
                    i+=1
                
                #Display frame, place scrollbar and tree
                frame.place(x=60, y=250)
                scrollbar.pack(side=RIGHT, fill=tk.Y)
                tree.pack()
                
                #submit
                connection.commit()
                connection.close()
                
            except sqlite3.OperationalError:
                error_label = tk.Label(window, text="Enter number!",fg="#0A0908", bg="#F2F4F3")
                error_label.place(x=400, y=250, anchor=tk.CENTER)
                error_label.after(2000,error_label.destroy())
            
        #Create button
        search_button = tk.Button(window, text="Search", command=search_number, bg="#5E503F", fg="#F2F4F3",  height = 1, width = 13)
        search_button.place(x=400, y=210, anchor = tk.CENTER)
    
    def by_id():
        
        global search_name_message_label 
        global search_number_message_label
        global search_id_message_label
        global search_number_label
        global search_fname_label 
        global search_lname_label
        global search_id_label 
        global fname_entry
        global lname_entry 
        global number_entry
        global id_entry 
        global counter
        
        if counter == 1:
            search_name_message_label.destroy()
            search_fname_label.destroy()
            search_lname_label.destroy()
            fname_entry.destroy()
            lname_entry.destroy()
        elif counter == 2:
            search_number_message_label.destroy()
            search_number_label.destroy()
            number_entry.destroy()
            
        counter = 3
        
        #Create labels
        search_id_message_label = tk.Label(window, text="Enter information: ",fg="#0A0908", bg="#F2F4F3")
        search_id_label = tk.Label(window, text="ID",fg="#0A0908", bg="#F2F4F3")
        #Display
        search_id_message_label.place(x=400, y=120, anchor=tk.CENTER)
        search_id_label.place(x=250, y=150, anchor=tk.CENTER)
        
        #Create entry
        id_entry = tk.Entry(window, width=35, border= 5)
        #Display
        id_entry.place(x=400, y=150, anchor=tk.CENTER)
        
        def search_id():
            """Function to search by id. Execution on search_button click."""
            
            try:
                #Connect
                connection = sqlite3.connect('address_book.db')
                cursor = connection.cursor()
                
                #Execute query
                cursor.execute("SELECT *, oid FROM contact WHERE oid = " + id_entry.get())
                records = cursor.fetchall()
                
                #Create frame to place tabel(treeview) and scrollbar   
                frame = tk.Frame(window)
                
                #Create scrollbar and place it in frame
                scrollbar = tk.Scrollbar(frame)
                
                #Crate table using treeview and place it in frame
                tree = ttk.Treeview(frame, selectmode="browse", yscrollcommand=scrollbar.set)
                    
                #Set scrollbar command to view tabel vertically
                scrollbar.config(command=tree.yview)
                    
                #Define table: columns (like in DB)
                tree['columns'] = ("First Name","Last Name","Address","Phone Number","Email","oid")
                    
                #Format columns, #0 is the column that treeview adds alone
                tree.column("#0", width=0)
                tree.column("First Name",anchor=tk.W, width=100)
                tree.column("Last Name", anchor=tk.W, width=100)
                tree.column("Address", anchor=tk.W, width=150)
                tree.column("Phone Number", anchor=tk.W, width=100)
                tree.column("Email", anchor=tk.W, width=200)
                tree.column("oid", anchor=tk.W, width=50)
                    
                #Format Headings (header row)
                tree.heading("#0", text="", anchor=tk.CENTER)
                tree.heading("First Name", text="First Name", anchor=tk.CENTER)
                tree.heading("Last Name", text="Last Name", anchor=tk.CENTER)
                tree.heading("Address", text="Address", anchor=tk.CENTER)
                tree.heading("Phone Number", text="Phone Number", anchor=tk.CENTER)
                tree.heading("Email", text="Email", anchor=tk.CENTER)
                tree.heading("oid", text="ID", anchor=tk.CENTER)
                    
                #Inserting data into rows from records (cursor.fetchall()), set counter "i" to add to specific row
                i=0
                for record in records:
                    tree.insert(parent='', index='end', iid=i, values=record)
                    i+=1
                
                #Display frame, place scrollbar and tree
                frame.place(x=60, y=250)
                scrollbar.pack(side=RIGHT, fill=tk.Y)
                tree.pack()
                
                #submit
                connection.commit()
                connection.close()
                
            except sqlite3.OperationalError:
                error_label = tk.Label(window, text="Enter ID!",fg="#0A0908", bg="#F2F4F3")
                error_label.place(x=400, y=250, anchor=tk.CENTER)
                error_label.after(2000,error_label.destroy())
        
        #Create button
        search_button = tk.Button(window, text="Search", command=search_id, bg="#5E503F", fg="#F2F4F3",  height = 1, width = 13)
        search_button.place(x=400, y=210, anchor = tk.CENTER)
        
    #Create label
    message_label = tk.Label(window, text="What would you like to search by?",fg="#0A0908", bg="#F2F4F3")
    message_label.place(x=400, y=50, anchor=tk.CENTER)
    
    #Create buttons: search ba name or number
    by_name_button = tk.Button(window, text="By name", command=by_name, bg="#5E503F", fg="#F2F4F3",  height = 1, width = 13)
    by_number_button = tk.Button(window, text="By number", command=by_number, bg="#5E503F", fg="#F2F4F3",  height = 1, width = 13)
    by_id_button = tk.Button(window, text="By ID", command=by_id, bg="#5E503F", fg="#F2F4F3",  height = 1, width = 13)
    by_name_button.place(x=280, y=90, anchor=tk.CENTER)
    by_number_button.place(x=400, y=90, anchor=tk.CENTER)
    by_id_button.place(x=520, y=90, anchor=tk.CENTER)
    
def delete_contact():
    """Function to delete a contact from DB using ID"""
    
    #Create new window
    window = Toplevel()
    window.title("Delete Contact")
    window.iconbitmap('images\\icon.ico')
    window.geometry("400x400")
    window.configure(background="#F2F4F3")
    
    #Create label
    message_label = tk.Label(window, text="Enter contact ID",fg="#0A0908", bg="#F2F4F3")
    message_label.place(x=200, y=200, anchor=tk.CENTER)
    
    #Create Entry for id
    id_entry = tk.Entry(window, width=35, border= 5)
    id_entry.place(x=200, y=230, anchor = tk.CENTER)
    
    def delete_sql():
        """Funtion to execute SQL delete. Execution od delete_button click."""
        
        try:
            #Connect
            connection = sqlite3.connect('address_book.db')
            cursor = connection.cursor()
            
            #Execute query
            cursor.execute("DELETE FROM contact where oid = " + id_entry.get())
            
            #Submit and close connection
            connection.commit()
            connection.close() 
            
            #Create label
            message_label = tk.Label(window, text="Contact deleted!",fg="#0A0908", bg="#F2F4F3")
            message_label.place(x=200, y=310, anchor=tk.CENTER)
            message_label.after(2000, message_label.destroy)
            
            #Clear entered ID
            id_entry.delete(0,tk.END)
            
        except sqlite3.OperationalError:
            message_label = tk.Label(window, text="Enter ID",fg="#0A0908", bg="#F2F4F3")
            message_label.place(x=200, y=310, anchor=tk.CENTER)
            message_label.after(2000, message_label.destroy)
            
    #Create delete button
    delete_button = tk.Button(window, text="Delete", command=delete_sql, bg="#5E503F", fg="#F2F4F3",  height = 1, width = 13)
    delete_button.place(x=200, y=280, anchor=tk.CENTER)  


#Create buttons: start and exit
start_button = tk.Button(root, text="Start", command=lambda:start(), bg="#5E503F", fg="#F2F4F3",  height = 1, width = 13)
exit_button = tk.Button(root, text="Exit", command=root.quit, bg="#5E503F", fg="#F2F4F3", height = 1, width = 13)
#Display
start_button.place(x=120, y=350, anchor=tk.CENTER)
exit_button.place(x=280, y=350, anchor=tk.CENTER)

#Run root window for program
root.mainloop()