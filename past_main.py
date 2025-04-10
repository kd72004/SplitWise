from user import User
from user_controller import UserController
from group_controller import GroupController
from expense_controller import ExpenseController
import json
result = []  
if __name__ == "__main__":
    group_controller = GroupController()
    user_controller = UserController()
    # new_user = User(user_name="sanjay")
    # user_id = user_controller.add_user(new_user)
    # fetched_user = user_controller.get_user(user_id)
    # if fetched_user:
    #     print(f"User Found: {fetched_user.get_user_name()}, ID: {fetched_user.get_user_id()}")
        
    
    # group realted adding a new group with nme and then addaing members into group nad then fetch add the data of that group and of that member 
    # 1. Create a new group
    # group_name = "france"
    # group_response = group_controller.create_group(group_name)
    # print(group_response)

    # # if "error" in group_response:
    # #     print(group_response)
    # #     exit()

    # group_id = '5bff8d95-0a4c-4ac1-8000-19431ba01510'
    
    # # 2. Add users to the group
    # user_ids = ["0a3d8f47-67da-432f-9de3-45e121240c12", "5ae547b7-04b6-4579-b788-6a6742d47db9", "8c7b45be-9c46-41ae-b909-1b8243bbbf13"]  # Replace with actual user IDs
    # for user_id in user_ids:
    #     add_response = group_controller.add_user_to_group(group_id, user_id)
    #     print(add_response)

    # # 3. Get groups for a specific user
    # user_id_to_check = "0a3d8f47-67da-432f-9de3-45e121240c12"  # Replace with an actual user ID
    # user_groups = group_controller.get_user_groups(user_id_to_check)
    # print(f"Groups for user {user_id_to_check}: {user_groups}")

    # 4. Get members of a specific group
    # group_id = "5bff8d95-0a4c-4ac1-8000-19431ba01510"

    # group_details = group_controller.get_group_members(group_id)

    # if "error" in group_details:
    #     print(group_details["error"])
    # else:
    #     group_name = group_details["group_name"]
    #     members = group_details["members"]
    #     print(f"Group Name: {group_name}")
    #     print("Members:")
    #     for member in members:
    #         print(f"  - ID: {member['user_id']}, Name: {member['user_name']}")
    # # 5. Delete the group
    # delete_response = group_controller.delete_group(group_id)
    # print(delete_response)
    
    # Remove a user from the group  
    # remove_response = group_controller.remove_user_from_group(group_id, user_to_remove)  here you have to pass groupid and user id and done 
    # print(remove_response)





# Example of calling the method with a group_id

# group_id = "5bff8d95-0a4c-4ac1-8000-19431ba01510"  # This could come from your session, input, or be generated
# name = "Dinner"
# paid_by = "0a3d8f47-67da-432f-9de3-45e121240c12"
# total_amount = 100.0
# split_type = "equal"
# user_shares = [
#     {"userid": "5ae547b7-04b6-4579-b788-6a6742d47db9", "amount": 50},
#     {"userid": "8c7b45be-9c46-41ae-b909-1b8243bbbf13", "amount": 50}
# ]

# # controller = ExpenseController()
# # expense_data = controller.create_expense(name, paid_by, total_amount, split_type, user_shares, group_id)

# # # This will return the expense data including the group_id
# # print(expense_data)

# controller = ExpenseController()
# expense_data = controller.create_expense(name, paid_by, total_amount, split_type, user_shares, group_id)

# # This will return the expense data including the group_id
# print(expense_data)

def get_result():
    expense_controller = ExpenseController()
    name = "Dinner"
    paid_by = "0a3d8f47-67da-432f-9de3-45e121240c12"
    total_amount = 100.00
    split_type = "unequal"
    group_id = "5bff8d95-0a4c-4ac1-8000-19431ba01510" 
    user_shares = [
        {"borrower_id": "5ae547b7-04b6-4579-b788-6a6742d47db9", "amount": 50.00},
        {"borrower_id": "8c7b45be-9c46-41ae-b909-1b8243bbbf13", "amount": 50.00}
    ]


    expense_data = expense_controller.create_expense(name, paid_by, total_amount, split_type, user_shares, group_id)
    split_transactions = expense_data.get("split_transactions", {})

    result = []  
    for borrower_id, details in split_transactions.items():
        result.append([borrower_id, details['paid_by'], details['amount']])

    print("Processed Result:", result)
    print("Group ID:", group_id)
    
    return result, group_id  

if __name__ == "__main__":
    get_result()
