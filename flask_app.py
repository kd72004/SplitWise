from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from user_controller import UserController
from group_controller import GroupController
from expense_controller import ExpenseController
from logic import BalanceCalculator
import logging

app = Flask(__name__)
app.secret_key = 'splitwise_secret_key_2024'

# Initialize controllers
user_controller = UserController()
group_controller = GroupController()
expense_controller = ExpenseController()
balance_calculator = BalanceCalculator()

logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Clear any existing session when accessing login page
        session.clear()
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        result = user_controller.login(username, password)
        if result['success']:
            session['user_id'] = result['user_id']
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(result['message'], 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        result = user_controller.register(username, email, password)
        if result['success']:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'error')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    groups = group_controller.get_user_groups(user_id)
    return render_template('dashboard.html', groups=groups, username=session['username'])

@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        group_name = request.form['group_name']
        user_id = session['user_id']
        
        result = group_controller.create_group(group_name, user_id)
        
        if result['success']:
            flash('Group created successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(result['message'], 'error')
    
    return render_template('create_group.html')

@app.route('/group/<group_id>')
def group_detail(group_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    group_info = group_controller.get_group_info(group_id)
    members = group_controller.get_group_members(group_id)
    expenses = expense_controller.get_group_expenses(group_id)
    
    return render_template('group_detail.html', 
                         group=group_info, 
                         members=members, 
                         expenses=expenses,
                         group_id=group_id)

@app.route('/add_member/<group_id>', methods=['GET', 'POST'])
def add_member(group_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = request.form['username']
        
        result = group_controller.add_member_by_username(group_id, username)
        if result['success']:
            flash('Member added successfully!', 'success')
        else:
            flash(result['message'], 'error')
        
        return redirect(url_for('group_detail', group_id=group_id))
    
    group_info = group_controller.get_group_info(group_id)
    return render_template('add_member.html', group=group_info, group_id=group_id)

@app.route('/add_expense/<group_id>', methods=['GET', 'POST'])
def add_expense(group_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    members = group_controller.get_group_members(group_id)
    
    if request.method == 'POST':
        description = request.form['description']
        total_amount = float(request.form['total_amount'])
        paid_by = int(request.form['paid_by'])
        split_type = request.form['split_type']
        
        if split_type == 'equal':
            # Equal split among all members
            member_ids = [m.user_id for m in members]
            result = expense_controller.create_expense(
                group_id, description, total_amount, paid_by, member_ids
            )
        else:
            # Custom split - get individual amounts
            member_amounts = {}
            for member in members:
                amount_key = f'amount_{member.user_id}'
                if amount_key in request.form and request.form[amount_key]:
                    member_amounts[member.user_id] = float(request.form[amount_key])
            
            result = expense_controller.create_custom_expense(
                group_id, description, total_amount, paid_by, member_amounts
            )
        
        if result['success']:
            flash('Expense added successfully!', 'success')
            return redirect(url_for('group_detail', group_id=group_id))
        else:
            flash(result['message'], 'error')
    
    group_info = group_controller.get_group_info(group_id)
    return render_template('add_expense.html', 
                         group=group_info, 
                         members=members, 
                         group_id=group_id)

@app.route('/settlements/<group_id>')
def settlements(group_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Process settlements
    settlements = balance_calculator.process_group_settlements(group_id)
    settlement_data = balance_calculator.get_group_settlements(group_id)
    
    group_info = group_controller.get_group_info(group_id)
    
    return render_template('settlements.html', 
                         settlements=settlement_data, 
                         group=group_info,
                         group_id=group_id)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)