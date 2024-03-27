import tkinter as tk
from tkinter import messagebox
import json
import TripPlanner as tripp
#import Booking as bk
import os

class Account:
    def __init__(self, username, password, file_path):
        self.username = username
        self.password = password
        self.file_path = file_path
        self.tps = [filename for filename in os.listdir('.') if filename.startswith(self.username)]

class LoginSystem:
    def __init__(self, file_path):
        self.accounts = {}  # Dictionary to store accounts and passwords
        self.file_path = file_path
        self.load_accounts()

    def load_accounts(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                for username, password in data.items():
                    self.accounts[username] = Account(username, password, self.file_path)

        except FileNotFoundError:
            pass

    def save_accounts(self):
        data = {account.username: account.password for account in self.accounts.values()}
        with open(self.file_path, 'w') as file:
            json.dump(data, file)
                    
    def create_account(self, username, password):
        if username not in self.accounts:
            self.accounts[username] = Account(username, password, self.file_path)
            self.save_accounts()
            return True
        else:
            return False  # Username already exists

    def login(self, username, password):
        if username in self.accounts:
            return self.accounts[username].password == password
        else:
            return False  # Username doesn't exist

class LoginSignupGUI:
    def __init__(self, root, login_system):
        self.root = root
        self.root.title("Trip Planner")
        self.root.geometry("300x180")
        self.login_system = login_system

        self.logged_in = False

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Log In", command=self.login)
        self.login_button.pack()

        self.signup_button = tk.Button(root, text="Sign Up", command=self.signup)
        self.signup_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.login_system.login(username, password):
            self.logged_in = True
            self.clear_window()
            self.logging_in()

            '''Write the code here'''
        else:
            messagebox.showerror("Incorrect!", "Login failed. Incorrect username or password.")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.login_system.create_account(username, password):
            messagebox.showinfo("New Account", "Account created successfully!")
        else:
            messagebox.showerror("Error", "Account creation failed. Username already exists.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def logging_in(self):
        username = self.username_entry.get()  # Fetch the logged-in username
        user_info = self.login_system.accounts[username]  # Fetch the user information from LoginSystem
        self.show_logged_in_view(user_info)

    def show_logged_in_view(self, user_info):
        for widget in self.root.winfo_children():
            widget.destroy()
        root = self.root
        root.title("Menu")
        root.geometry("300x200")

        welcome = tk.Label(root, text=f"Hello, {user_info.username}!\nSelect one of the following options:")
        welcome.pack()
        button1 = tk.Button(root, text="Check History of Trips", width=20, command=lambda: self.checkHistory(user_info))
        button1.pack()
        button2 = tk.Button(root, text="Add New Trip", width=20, command=lambda: self.addNewTrip(user_info))
        button2.pack()
        button3 = tk.Button(root, text="Delete Trip", width=20, command=lambda: self.deleteTrip(user_info))
        button3.pack()
        button4 = tk.Button(root, text="Log Out", width=20, command=lambda: self.logOut())
        button4.pack()
        #print("TPS:", user_info.tps)
        
    '''def booking(self):
        book = bk.Booking(self.root)
        book.bookingGUI()'''

    def logOut(self):
        self.root.destroy()

    def checkHistory(self, user_info):
        user_info.tps = [filename for filename in os.listdir('.') if filename.startswith(user_info.username + '_')]
        root = tk.Toplevel(self.root)
        root.title("History")
        root.geometry("500x250")

        def display_dictionary(dictionary):
            r = tk.Toplevel(root)
            r.title("Trip Plan Viewer")

            text_widget = tk.Text(r, wrap='word', height=20, width=50)
            text_widget.pack(expand=True, fill='both')

            def display_dict(dict_to_display):
                indent = 0
                base_currency = ""
                for key, value in dict_to_display.items():
                    if key == "Base Currency":
                        base_currency = value
                    text_widget.insert(tk.END, ' ' * indent + str(key) + ': ')
                    if isinstance(value, list):
                        count = 0
                        for i in value:
                            count += 1
                            text_widget.insert(tk.END, f'\n{count}. Destination:\n')
                            if isinstance(i, dict):
                                indent = 4
                                for j, k in i.items():
                                    text_widget.insert(tk.END, ' ' * indent + str(j) + ': ')
                                    if isinstance(k, float) and j != "Exchange Rate":
                                        text_widget.insert(tk.END, f"{k:,.2f} {base_currency}\n")
                                    elif j == "Exchange Rate":
                                        text_widget.insert(tk.END, f"{k:,.2f}\n")
                                    else:
                                        text_widget.insert(tk.END, str(k) + '\n')
                    else:
                        if isinstance(value, float) and key != "Exchange Rate":
                            text_widget.insert(tk.END, f"{value:,.2f} {base_currency}\n")
                        elif key == "Exchange Rate":
                            text_widget.insert(tk.END, f"{value:,.2f}\n")
                        else:
                            text_widget.insert(tk.END, str(value) + '\n')

            display_dict(dictionary)

        def checkTripPlan():
            selected_file = listbox.get(tk.ACTIVE)
            if selected_file:
                file_path = os.path.join('.', selected_file)
                data = {}
                with open(file_path, 'r') as file:
                    data = json.load(file)
                display_dictionary(data)
                    
        listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        listbox.pack()
        listbox.config(width=50)
        listbox.delete(0, tk.END)
        for elem in user_info.tps:
            listbox.insert(tk.END, elem)

        checkTP = tk.Button(root, text="Check Trip Plan", command=checkTripPlan)
        checkTP.pack()

        #print(user_info.tps)
        #print("History Checked!")

    def addNewTrip(self, user_info):
        tp = tripp.TripPlanner(user_info.username)
        tp.create_trip_planner(self.root)
        #print("New Trip Added")

    def deleteTrip(self, user_info):
        user_info.tps = [filename for filename in os.listdir('.') if filename.startswith(user_info.username)]
        root = tk.Toplevel(self.root)
        root.title("Delete Trip Plan")
        root.geometry("500x250")

        def delete_selected_file():
            selected_file = listbox.get(tk.ACTIVE)
            if selected_file:
                file_path = os.path.join('.', selected_file)
                os.remove(file_path)
                user_info.tps.remove(selected_file)
                listbox.delete(tk.ACTIVE)

        listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        listbox.pack()
        listbox.config(width=50)
        listbox.delete(0, tk.END)
        for elem in user_info.tps:
            listbox.insert(tk.END, elem)

        deleteButton = tk.Button(root, text="Delete Trip Plan", command=delete_selected_file)
        deleteButton.pack()

        #print(user_info.tps)
        #print("TP Deleted!")