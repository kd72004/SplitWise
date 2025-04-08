import customtkinter as ctk
from user_controller import UserController  # Import the UserController
from user import User  # Import User model

# Initialize the database controller
user_controller = UserController()

# Main App Class
class SplitwiseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Splitwise - Login or Register")
        self.geometry("500x400")
        ctk.set_appearance_mode("dark")  # Dark mode UI

        self.create_login_ui()

    # 📌 Function to show login UI
    def create_login_ui(self):
        self.clear_screen()

        ctk.CTkLabel(self, text="Login", font=("Arial", 20)).pack(pady=20)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Enter username")
        self.username_entry.pack(pady=10)

        login_btn = ctk.CTkButton(self, text="Login", command=self.login_user)
        login_btn.pack(pady=10)

        switch_btn = ctk.CTkButton(self, text="New User? Register Here", command=self.create_register_ui)
        switch_btn.pack(pady=10)

    # 📌 Function to show register UI
    def create_register_ui(self):
        self.clear_screen()

        ctk.CTkLabel(self, text="Register", font=("Arial", 20)).pack(pady=20)

        self.new_username_entry = ctk.CTkEntry(self, placeholder_text="Choose a username")
        self.new_username_entry.pack(pady=10)

        register_btn = ctk.CTkButton(self, text="Register", command=self.register_user)
        register_btn.pack(pady=10)

        switch_btn = ctk.CTkButton(self, text="Already have an account? Login", command=self.create_login_ui)
        switch_btn.pack(pady=10)

    # 📌 Function to handle user registration
    def register_user(self):
        username = self.new_username_entry.get().strip()
        if username:
            new_user = User(user_name=username)
            user_controller.add_user(new_user)
            ctk.CTkLabel(self, text=f"User {username} registered!").pack(pady=10)
            self.create_login_ui()  # Go back to login page
        else:
            ctk.CTkLabel(self, text="Username cannot be empty!", fg_color="red").pack(pady=10)

    # 📌 Function to handle user login
    def login_user(self):
        username = self.username_entry.get().strip()
        users = user_controller.get_all_users()

        for user in users:
            if user.get_user_name() == username:
                self.show_dashboard(username)
                return
        
        ctk.CTkLabel(self, text="User not found! Please register.", fg_color="red").pack(pady=10)

    # 📌 Function to show dashboard
    def show_dashboard(self, username):
        self.clear_screen()
        ctk.CTkLabel(self, text=f"Welcome, {username}!", font=("Arial", 20)).pack(pady=20)
        logout_btn = ctk.CTkButton(self, text="Logout", command=self.create_login_ui)
        logout_btn.pack(pady=20)

    # 📌 Utility function to clear UI
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

# Run the App
if __name__ == "__main__":
    app = SplitwiseApp()
    app.mainloop()
