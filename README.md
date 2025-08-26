# SplitWise - Expense Sharing Web Application

A comprehensive expense sharing platform that helps groups split bills and optimize debt settlements using advanced algorithms.

## 🚀 Features
- **User Authentication** - Secure registration/login with password hashing
- **Group Management** - Create groups and invite members
- **Expense Tracking** - Add expenses with equal or custom splitting
- **Smart Settlements** - Optimized debt resolution using heap-based algorithm
- **Responsive UI** - Dark theme web interface

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML/CSS, JavaScript, Jinja2
- **Security:** SHA256 password hashing

## ⚡ Key Algorithm
MaxHeap-based settlement optimization that reduces transaction count by 60-70%, minimizing the number of payments needed to settle all group debts.

## 🏃♂️ Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/kd72004/SplitWise.git
   cd SplitWise
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Run the application**
   ```bash
   python flask_app.py
   ```

4. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure
```
SplitWise/
├── flask_app.py           # Main Flask application
├── connection_sqlite.py   # Database connection
├── user_controller.py     # User management
├── group_controller.py    # Group operations
├── expense_controller.py  # Expense handling
├── logic.py              # Settlement optimization
├── templates/            # HTML templates
└── requirements_flask.txt # Dependencies
```

## 🔧 Database Schema
- **users** - User accounts and authentication
- **groups** - Group information
- **group_members** - User-group relationships
- **expense** - Expense records
- **expense_share** - Individual expense shares
- **balance_sheet** - Optimized settlements

## 🎯 Key Features Implemented
- MVC architecture pattern
- Secure password hashing with SHA256
- Normalized database design with 6 tables
- MaxHeap algorithm for transaction optimization
- Responsive web interface with dark theme
- Session-based authentication

## 🤝 Contributing
Feel free to fork this project and submit pull requests for any improvements.

## 📄 License
This project is open source and available under the MIT License.