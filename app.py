import customtkinter as ctk
from user_controller import UserController 
from group_controller import GroupController
from expense_controller import ExpenseController
from user import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SplitwiseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Splitwise - Expense Sharing App")
        self.geometry("600x500")
        ctk.set_appearance_mode("dark")
        
        self.user_controller = UserController()
        self.group_controller = GroupController()
        self.expense_controller = ExpenseController()
        self.current_user = None
        self.message_label = None
        
        self.create_login_ui()

    def create_login_ui(self):
        self.clear_screen()
        
        # Title
        title = ctk.CTkLabel(self, text="Splitwise", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Login section
        login_frame = ctk.CTkFrame(self)
        login_frame.pack(pady=20, padx=40, fill="x")
        
        ctk.CTkLabel(login_frame, text="Login", font=("Arial", 18)).pack(pady=10)
        
        self.username_entry = ctk.CTkEntry(login_frame, placeholder_text="Enter username", width=300)
        self.username_entry.pack(pady=5)
        
        login_btn = ctk.CTkButton(login_frame, text="Login", command=self.login_user, width=200)
        login_btn.pack(pady=10)
        
        # Register section
        register_frame = ctk.CTkFrame(self)
        register_frame.pack(pady=10, padx=40, fill="x")
        
        ctk.CTkLabel(register_frame, text="New User", font=("Arial", 18)).pack(pady=10)
        
        self.new_username_entry = ctk.CTkEntry(register_frame, placeholder_text="Choose username", width=300)
        self.new_username_entry.pack(pady=5)
        
        register_btn = ctk.CTkButton(register_frame, text="Register", command=self.register_user, width=200)
        register_btn.pack(pady=10)
        
        # Message label
        self.message_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.message_label.pack(pady=10)

    def register_user(self):
        username = self.new_username_entry.get().strip()
        if not username:
            self.show_message("Username cannot be empty!", "red")
            return
            
        try:
            new_user = User(user_name=username)
            self.user_controller.add_user(new_user)
            self.show_message(f"User '{username}' registered successfully!", "green")
            self.new_username_entry.delete(0, 'end')
        except ValueError as e:
            self.show_message(str(e), "red")
        except Exception as e:
            self.show_message("Registration failed. Please try again.", "red")
            logger.error(f"Registration error: {e}")

    def login_user(self):
        username = self.username_entry.get().strip()
        if not username:
            self.show_message("Username cannot be empty!", "red")
            return
            
        try:
            users = self.user_controller.get_all_users()
            for user in users:
                if user.get_user_name() == username:
                    self.current_user = user
                    self.show_dashboard()
                    return
            self.show_message("User not found! Please register first.", "red")
        except Exception as e:
            self.show_message("Login failed. Please try again.", "red")
            logger.error(f"Login error: {e}")

    def show_dashboard(self):
        self.clear_screen()
        
        # Welcome header
        welcome = ctk.CTkLabel(self, text=f"Welcome, {self.current_user.get_user_name()}!", 
                              font=("Arial", 20, "bold"))
        welcome.pack(pady=20)
        
        # Main buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        ctk.CTkButton(button_frame, text="Create Group", command=self.show_create_group, 
                     width=200, height=40).pack(pady=10)
        
        ctk.CTkButton(button_frame, text="My Groups", command=self.show_my_groups, 
                     width=200, height=40).pack(pady=10)
        
        ctk.CTkButton(button_frame, text="Add Expense", command=self.show_add_expense, 
                     width=200, height=40).pack(pady=10)
        
        ctk.CTkButton(button_frame, text="Logout", command=self.logout, 
                     width=200, height=40).pack(pady=20)
        
        # Message label
        self.message_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.message_label.pack(pady=10)

    def show_create_group(self):
        self.clear_screen()
        
        ctk.CTkLabel(self, text="Create New Group", font=("Arial", 20)).pack(pady=20)
        
        self.group_name_entry = ctk.CTkEntry(self, placeholder_text="Group name", width=300)
        self.group_name_entry.pack(pady=10)
        
        create_btn = ctk.CTkButton(self, text="Create Group", command=self.create_group, width=200)
        create_btn.pack(pady=10)
        
        back_btn = ctk.CTkButton(self, text="Back to Dashboard", command=self.show_dashboard, width=200)
        back_btn.pack(pady=10)
        
        self.message_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.message_label.pack(pady=10)

    def create_group(self):
        group_name = self.group_name_entry.get().strip()
        if not group_name:
            self.show_message("Group name cannot be empty!", "red")
            return
            
        try:
            result = self.group_controller.create_group(group_name)
            if "error" in result:
                self.show_message(result["error"], "red")
            else:
                # Add current user to the group
                group_id = result["group_id"]
                self.group_controller.add_user_to_group(group_id, self.current_user.get_user_id())
                self.show_message(f"Group '{group_name}' created successfully!", "green")
                self.group_name_entry.delete(0, 'end')
        except Exception as e:
            self.show_message("Failed to create group. Please try again.", "red")
            logger.error(f"Group creation error: {e}")

    def show_my_groups(self):
        self.clear_screen()
        
        ctk.CTkLabel(self, text="My Groups", font=("Arial", 20)).pack(pady=20)
        
        try:
            result = self.group_controller.get_user_groups(self.current_user.get_user_id())
            if "error" in result:
                self.show_message(result["error"], "red")
            else:
                groups = result.get("groups", [])
                if not groups:
                    ctk.CTkLabel(self, text="You are not in any groups yet.", font=("Arial", 14)).pack(pady=20)
                else:
                    for group in groups:
                        group_frame = ctk.CTkFrame(self)
                        group_frame.pack(pady=5, padx=40, fill="x")
                        
                        # Group name
                        name_label = ctk.CTkLabel(group_frame, text=group["group_name"], font=("Arial", 16))
                        name_label.pack(pady=5)
                        
                        # Buttons frame
                        btn_frame = ctk.CTkFrame(group_frame)
                        btn_frame.pack(pady=5, fill="x")
                        
                        # Add member button
                        add_member_btn = ctk.CTkButton(btn_frame, text="Add Member", 
                                                     command=lambda gid=group["group_id"]: self.show_add_member(gid),
                                                     width=120, height=30)
                        add_member_btn.pack(side="left", padx=5)
                        
                        # View settlements button
                        settlements_btn = ctk.CTkButton(btn_frame, text="View Settlements", 
                                                       command=lambda gid=group["group_id"]: self.show_settlements(gid),
                                                       width=120, height=30)
                        settlements_btn.pack(side="left", padx=5)
                        
        except Exception as e:
            self.show_message("Failed to load groups.", "red")
            logger.error(f"Groups loading error: {e}")
        
        back_btn = ctk.CTkButton(self, text="Back to Dashboard", command=self.show_dashboard, width=200)
        back_btn.pack(pady=20)
        
        self.message_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.message_label.pack(pady=10)

    def show_add_expense(self):
        self.clear_screen()
        
        ctk.CTkLabel(self, text="Add Expense", font=("Arial", 20)).pack(pady=20)
        
        # Get user's groups first
        try:
            result = self.group_controller.get_user_groups(self.current_user.get_user_id())
            if "error" in result or not result.get("groups"):
                ctk.CTkLabel(self, text="You need to be in a group to add expenses.", font=("Arial", 14)).pack(pady=20)
                back_btn = ctk.CTkButton(self, text="Back to Dashboard", command=self.show_dashboard, width=200)
                back_btn.pack(pady=20)
                return
            
            self.groups = result["groups"]
            
            # Group selection
            ctk.CTkLabel(self, text="Select Group:", font=("Arial", 14)).pack(pady=5)
            self.group_var = ctk.StringVar(value=self.groups[0]["group_name"])
            group_menu = ctk.CTkOptionMenu(self, variable=self.group_var, 
                                         values=[g["group_name"] for g in self.groups],
                                         command=self.on_group_change)
            group_menu.pack(pady=5)
            
            # Expense details
            ctk.CTkLabel(self, text="Expense Name:", font=("Arial", 14)).pack(pady=5)
            self.expense_name_entry = ctk.CTkEntry(self, placeholder_text="Enter expense name", width=300)
            self.expense_name_entry.pack(pady=5)
            
            ctk.CTkLabel(self, text="Total Amount:", font=("Arial", 14)).pack(pady=5)
            self.amount_entry = ctk.CTkEntry(self, placeholder_text="Enter amount", width=300)
            self.amount_entry.pack(pady=5)
            
            # Split type
            ctk.CTkLabel(self, text="Split Type:", font=("Arial", 14)).pack(pady=5)
            self.split_var = ctk.StringVar(value="equal")
            split_menu = ctk.CTkOptionMenu(self, variable=self.split_var, 
                                         values=["equal", "custom"],
                                         command=self.on_split_type_change)
            split_menu.pack(pady=5)
            
            # Member selection frame
            self.member_frame = ctk.CTkScrollableFrame(self, width=500, height=200)
            self.member_frame.pack(pady=10, padx=20, fill="both")
            
            # Load initial members
            self.load_group_members()
            
            # Buttons
            add_btn = ctk.CTkButton(self, text="Add Expense", command=self.add_custom_expense, width=200)
            add_btn.pack(pady=10)
            
            back_btn = ctk.CTkButton(self, text="Back to Dashboard", command=self.show_dashboard, width=200)
            back_btn.pack(pady=10)
            
            self.message_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
            self.message_label.pack(pady=10)
            
        except Exception as e:
            self.show_message("Failed to load groups.", "red")
            logger.error(f"Add expense error: {e}")

    def logout(self):
        self.current_user = None
        self.create_login_ui()

    def show_message(self, message, color="white"):
        if self.message_label:
            self.message_label.configure(text=message, text_color=color)

    def on_group_change(self, selected_group_name):
        """Called when group selection changes"""
        self.load_group_members()
    
    def on_split_type_change(self, selected_split_type):
        """Called when split type changes"""
        self.load_group_members()
    
    def load_group_members(self):
        """Load and display group members with checkboxes and amount entries"""
        # Clear existing widgets
        for widget in self.member_frame.winfo_children():
            widget.destroy()
        
        try:
            # Get selected group
            selected_group_name = self.group_var.get()
            selected_group = next((g for g in self.groups if g["group_name"] == selected_group_name), None)
            
            if not selected_group:
                return
            
            # Get group members
            members_result = self.group_controller.get_group_members(selected_group["group_id"])
            if "error" in members_result:
                return
            
            members = members_result["members"]
            self.member_widgets = []
            
            split_type = self.split_var.get()
            
            if split_type == "equal":
                ctk.CTkLabel(self.member_frame, text="Select Members (Equal Split):", 
                            font=("Arial", 14, "bold")).pack(pady=10)
            else:
                ctk.CTkLabel(self.member_frame, text="Select Members and Enter Amounts:", 
                            font=("Arial", 14, "bold")).pack(pady=10)
            
            for member in members:
                member_frame = ctk.CTkFrame(self.member_frame)
                member_frame.pack(pady=5, padx=10, fill="x")
                
                # Checkbox for member selection
                checkbox_var = ctk.BooleanVar(value=True)
                checkbox = ctk.CTkCheckBox(member_frame, text=member["user_name"], 
                                         variable=checkbox_var, width=150)
                checkbox.pack(side="left", padx=10, pady=10)
                
                # Amount entry (only for custom split)
                if split_type == "custom":
                    amount_entry = ctk.CTkEntry(member_frame, placeholder_text="Amount", width=100)
                    amount_entry.pack(side="right", padx=10, pady=10)
                else:
                    amount_entry = None
                
                self.member_widgets.append({
                    "user_id": member["user_id"],
                    "user_name": member["user_name"],
                    "checkbox": checkbox_var,
                    "amount_entry": amount_entry
                })
                
        except Exception as e:
            logger.error(f"Error loading members: {e}")
    
    def add_custom_expense(self):
        expense_name = self.expense_name_entry.get().strip()
        total_amount_str = self.amount_entry.get().strip()
        
        if not expense_name:
            self.show_message("Please enter expense name!", "red")
            return
        
        try:
            # Get selected group
            selected_group_name = self.group_var.get()
            selected_group = next((g for g in self.groups if g["group_name"] == selected_group_name), None)
            
            if not selected_group:
                self.show_message("Selected group not found!", "red")
                return
            
            # Get selected members and their amounts
            selected_members = []
            total_custom_amount = 0
            split_type = self.split_var.get()
            
            for widget_info in self.member_widgets:
                if widget_info["checkbox"].get():  # If member is selected
                    if split_type == "custom":
                        # For custom split, get individual amounts
                        amount_str = widget_info["amount_entry"].get().strip()
                        if not amount_str:
                            self.show_message(f"Please enter amount for {widget_info['user_name']}!", "red")
                            return
                        
                        try:
                            amount = float(amount_str)
                            if amount <= 0:
                                self.show_message(f"Amount for {widget_info['user_name']} must be positive!", "red")
                                return
                            
                            selected_members.append({
                                "borrower_id": widget_info["user_id"],
                                "amount": amount
                            })
                            total_custom_amount += amount
                            
                        except ValueError:
                            self.show_message(f"Invalid amount for {widget_info['user_name']}!", "red")
                            return
                    else:
                        # For equal split, just add member (amount will be calculated later)
                        selected_members.append({
                            "borrower_id": widget_info["user_id"],
                            "amount": 0  # Placeholder, will be calculated
                        })
            
            if not selected_members:
                self.show_message("Please select at least one member!", "red")
                return
            
            # Determine total amount based on split type
            if split_type == "equal":
                if not total_amount_str:
                    self.show_message("Please enter total amount for equal split!", "red")
                    return
                
                total_amount = float(total_amount_str)
                if total_amount <= 0:
                    self.show_message("Total amount must be positive!", "red")
                    return
                
                # Calculate equal amounts for each selected member
                share_amount = total_amount / len(selected_members)
                for member in selected_members:
                    member["amount"] = share_amount
            else:
                # Custom split - use entered amounts
                total_amount = total_custom_amount
            
            # Create expense
            expense_result = self.expense_controller.create_expense(
                name=expense_name,
                paid_by=self.current_user.get_user_id(),
                total_amount=total_amount,
                split_type="unequal",  # Always use unequal for custom amounts
                user_shares=selected_members,
                group_id=selected_group["group_id"]
            )
            
            self.show_message(f"Expense '{expense_name}' added successfully! Total: ${total_amount:.2f}", "green")
            
            # Clear form
            self.expense_name_entry.delete(0, 'end')
            self.amount_entry.delete(0, 'end')
            
            # Reset member amounts (only for custom split)
            for widget_info in self.member_widgets:
                if widget_info["amount_entry"]:
                    widget_info["amount_entry"].delete(0, 'end')
            
        except ValueError:
            self.show_message("Please enter valid amounts!", "red")
        except Exception as e:
            self.show_message("Failed to add expense. Please try again.", "red")
            logger.error(f"Add expense error: {e}")
    
    def show_add_member(self, group_id):
        self.clear_screen()
        
        ctk.CTkLabel(self, text="Add Member to Group", font=("Arial", 20)).pack(pady=20)
        
        # Get all users
        try:
            all_users = self.user_controller.get_all_users()
            if not all_users:
                ctk.CTkLabel(self, text="No users available to add.", font=("Arial", 14)).pack(pady=20)
            else:
                ctk.CTkLabel(self, text="Select User:", font=("Arial", 14)).pack(pady=5)
                self.user_var = ctk.StringVar(value=all_users[0].get_user_name())
                user_menu = ctk.CTkOptionMenu(self, variable=self.user_var,
                                            values=[user.get_user_name() for user in all_users])
                user_menu.pack(pady=5)
                
                add_btn = ctk.CTkButton(self, text="Add Member", 
                                      command=lambda: self.add_member_to_group(group_id, all_users), 
                                      width=200)
                add_btn.pack(pady=10)
                
        except Exception as e:
            self.show_message("Failed to load users.", "red")
            logger.error(f"Add member error: {e}")
        
        back_btn = ctk.CTkButton(self, text="Back to Groups", command=self.show_my_groups, width=200)
        back_btn.pack(pady=10)
        
        self.message_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.message_label.pack(pady=10)
    
    def add_member_to_group(self, group_id, all_users):
        try:
            selected_username = self.user_var.get()
            selected_user = next((user for user in all_users if user.get_user_name() == selected_username), None)
            
            if not selected_user:
                self.show_message("Selected user not found!", "red")
                return
                
            result = self.group_controller.add_user_to_group(group_id, selected_user.get_user_id())
            if "error" in result:
                self.show_message(result["error"], "red")
            else:
                self.show_message(f"User '{selected_username}' added to group!", "green")
                
        except Exception as e:
            self.show_message("Failed to add member.", "red")
            logger.error(f"Add member error: {e}")
    
    def show_settlements(self, group_id):
        self.clear_screen()
        
        ctk.CTkLabel(self, text="Group Settlements", font=("Arial", 20)).pack(pady=20)
        
        try:
            from logic import BalanceCalculator
            calculator = BalanceCalculator()
            
            # Get settlements for this group
            settlements = calculator.get_group_settlements(group_id)
            
            if not settlements:
                ctk.CTkLabel(self, text="No settlements found. All debts are settled!", 
                           font=("Arial", 14)).pack(pady=20)
            else:
                # Create scrollable frame for settlements
                scroll_frame = ctk.CTkScrollableFrame(self, width=500, height=300)
                scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)
                
                for settlement in settlements:
                    settlement_frame = ctk.CTkFrame(scroll_frame)
                    settlement_frame.pack(pady=5, padx=10, fill="x")
                    
                    settlement_text = f"{settlement['borrower_name']} owes ${settlement['amount']:.2f} to {settlement['receiver_name']}"
                    ctk.CTkLabel(settlement_frame, text=settlement_text, font=("Arial", 14)).pack(pady=10)
            
            # Optimize settlements button
            optimize_btn = ctk.CTkButton(self, text="Optimize Settlements", 
                                       command=lambda: self.optimize_settlements(group_id), 
                                       width=200)
            optimize_btn.pack(pady=10)
            
        except Exception as e:
            self.show_message("Failed to load settlements.", "red")
            logger.error(f"Settlements error: {e}")
        
        back_btn = ctk.CTkButton(self, text="Back to Groups", command=self.show_my_groups, width=200)
        back_btn.pack(pady=10)
        
        self.message_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.message_label.pack(pady=10)
    
    def optimize_settlements(self, group_id):
        try:
            from logic import BalanceCalculator
            calculator = BalanceCalculator()
            
            # Process and optimize settlements for the group
            optimized_settlements = calculator.process_group_settlements(group_id)
            
            if not optimized_settlements:
                self.show_message("No settlements needed - all debts are balanced!", "green")
            else:
                self.show_message(f"Settlements optimized! {len(optimized_settlements)} transactions needed.", "green")
            
            # Refresh the settlements view
            self.show_settlements(group_id)
            
        except Exception as e:
            self.show_message("Failed to optimize settlements.", "red")
            logger.error(f"Optimization error: {e}")

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = SplitwiseApp()
    app.mainloop()