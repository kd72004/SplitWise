import customtkinter as ctk
from user_controller import UserController 
from user import User  
user_controller = UserController()


class SplitwiseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Splitwise - Login or Register")
        self.geometry("500x400")
        ctk.set_appearance_mode("dark")  

        self.create_login_ui()


    def create_login_ui(self):
        self.clear_screen()

        ctk.CTkLabel(self, text="Login", font=("Arial", 20)).pack(pady=20)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Enter username")
        self.username_entry.pack(pady=10)

        login_btn = ctk.CTkButton(self, text="Login", command=self.login_user)
        login_btn.pack(pady=10)

        switch_btn = ctk.CTkButton(self, text="New User? Register Here", command=self.create_register_ui)
        switch_btn.pack(pady=10)

 
    def create_register_ui(self):
        self.clear_screen()

        ctk.CTkLabel(self, text="Register", font=("Arial", 20)).pack(pady=20)

        self.new_username_entry = ctk.CTkEntry(self, placeholder_text="Choose a username")
        self.new_username_entry.pack(pady=10)

        register_btn = ctk.CTkButton(self, text="Register", command=self.register_user)
        register_btn.pack(pady=10)

        switch_btn = ctk.CTkButton(self, text="Already have an account? Login", command=self.create_login_ui)
        switch_btn.pack(pady=10)


    def register_user(self):
        username = self.new_username_entry.get().strip()
        if username:
            new_user = User(user_name=username)
            user_controller.add_user(new_user)
            ctk.CTkLabel(self, text=f"User {username} registered!").pack(pady=10)
            self.create_login_ui()  # Go back to login page
        else:
            ctk.CTkLabel(self, text="Username cannot be empty!", fg_color="red").pack(pady=10)

    def login_user(self):
        username = self.username_entry.get().strip()
        users = user_controller.get_all_users()

        for user in users:
            if user.get_user_name() == username:
                self.show_dashboard(username)
                return
        
        ctk.CTkLabel(self, text="User not found! Please register.", fg_color="red").pack(pady=10)


    def show_dashboard(self, username):
        self.clear_screen()
        ctk.CTkLabel(self, text=f"Welcome, {username}!", font=("Arial", 20)).pack(pady=20)
        logout_btn = ctk.CTkButton(self, text="Logout", command=self.create_login_ui)
        logout_btn.pack(pady=20)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = SplitwiseApp()
    app.mainloop()
