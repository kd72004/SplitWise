import tkinter as tk
import customtkinter as ctk
from user_controller import UserController
from user import User


user_controller = UserController()

app = ctk.CTk()
app.geometry("400x500")
app.title("User Authentication")
ctk.set_appearance_mode("dark") 


main_frame = ctk.CTkFrame(app)
main_frame.pack(pady=40, padx=20, fill="both", expand=True)

def register_user():
    user_name = entry_username.get()
    if user_name:
        new_user = User(user_name=user_name)
        user_id = user_controller.add_user(new_user)
        lbl_message.configure(text=f"User Created! ID: {user_id}", text_color="green")
    else:
        lbl_message.configure(text="Enter a username!", text_color="red")

def login_user():
    user_id = entry_user_id.get()
    user = user_controller.get_user(user_id)
    if user:
        lbl_message.configure(text=f"Welcome {user.get_user_name()}!", text_color="green")
        show_dashboard()
    else:
        lbl_message.configure(text="User not found!", text_color="red")

def show_dashboard():
    for widget in main_frame.winfo_children(): 
        widget.destroy()
    lbl_dashboard = ctk.CTkLabel(main_frame, text="Dashboard", font=("Arial", 20))
    lbl_dashboard.pack(pady=20)
    btn_logout = ctk.CTkButton(main_frame, text="Logout", command=show_main_screen)
    btn_logout.pack()

def show_main_screen():
    for widget in main_frame.winfo_children(): 
        widget.destroy()
    create_login_ui()
    create_register_ui()

# UI Components
lbl_title = ctk.CTkLabel(main_frame, text="User Authentication", font=("Arial", 22))
lbl_title.pack(pady=10)

lbl_message = ctk.CTkLabel(main_frame, text="", font=("Arial", 14))
lbl_message.pack()

def create_login_ui():
    global entry_user_id
    lbl_login = ctk.CTkLabel(main_frame, text="Login", font=("Arial", 18))
    lbl_login.pack(pady=10)
    entry_user_id = ctk.CTkEntry(main_frame, placeholder_text="Enter User ID")
    entry_user_id.pack()
    btn_login = ctk.CTkButton(main_frame, text="Login", command=login_user)
    btn_login.pack(pady=5)


def create_register_ui():
    global entry_username
    lbl_register = ctk.CTkLabel(main_frame, text="Register", font=("Arial", 18))
    lbl_register.pack(pady=10)
    entry_username = ctk.CTkEntry(main_frame, placeholder_text="Enter Username")
    entry_username.pack()
    btn_register = ctk.CTkButton(main_frame, text="Create User", command=register_user)
    btn_register.pack(pady=5)


create_login_ui()
create_register_ui()

app.mainloop()
