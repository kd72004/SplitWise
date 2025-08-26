#!/usr/bin/env python3
"""
Simple web backend to view SplitWise data via browser
Run this and go to http://localhost:8000 to view data
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from connection_sqlite import Database
import json
import urllib.parse

class SplitWiseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.serve_dashboard()
        elif self.path == '/api/users':
            self.serve_users()
        elif self.path == '/api/groups':
            self.serve_groups()
        elif self.path == '/api/expenses':
            self.serve_expenses()
        elif self.path == '/api/settlements':
            self.serve_settlements()
        elif self.path == '/api/stats':
            self.serve_stats()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>SplitWise Backend Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .card { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; text-align: center; }
                .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
                .stat-card { background: #3498db; color: white; padding: 20px; border-radius: 8px; text-align: center; }
                .stat-number { font-size: 2em; font-weight: bold; }
                .nav { display: flex; gap: 10px; margin: 20px 0; }
                .nav button { padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
                .nav button:hover { background: #2980b9; }
                .data-section { display: none; }
                .data-section.active { display: block; }
                table { width: 100%; border-collapse: collapse; margin-top: 10px; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background: #f8f9fa; font-weight: bold; }
                .expense-item { border-left: 4px solid #3498db; padding-left: 15px; margin: 10px 0; }
                .settlement-item { border-left: 4px solid #e74c3c; padding-left: 15px; margin: 10px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>SplitWise Backend Dashboard</h1>
                    <p>Database Management & Analytics</p>
                </div>
                
                <div class="card">
                    <div id="stats" class="stats"></div>
                </div>
                
                <div class="nav">
                    <button onclick="showSection('users')">Users</button>
                    <button onclick="showSection('groups')">Groups</button>
                    <button onclick="showSection('expenses')">Expenses</button>
                    <button onclick="showSection('settlements')">Settlements</button>
                </div>
                
                <div id="users" class="card data-section">
                    <h2>Users</h2>
                    <div id="users-data"></div>
                </div>
                
                <div id="groups" class="card data-section">
                    <h2>Groups</h2>
                    <div id="groups-data"></div>
                </div>
                
                <div id="expenses" class="card data-section">
                    <h2>Expenses</h2>
                    <div id="expenses-data"></div>
                </div>
                
                <div id="settlements" class="card data-section">
                    <h2>Optimized Settlements</h2>
                    <div id="settlements-data"></div>
                </div>
            </div>
            
            <script>
                async function loadStats() {
                    const response = await fetch('/api/stats');
                    const stats = await response.json();
                    document.getElementById('stats').innerHTML = `
                        <div class="stat-card">
                            <div class="stat-number">${stats.users}</div>
                            <div>Total Users</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${stats.groups}</div>
                            <div>Total Groups</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${stats.expenses}</div>
                            <div>Total Expenses</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">$${stats.total_amount}</div>
                            <div>Total Amount</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${stats.settlements}</div>
                            <div>Active Settlements</div>
                        </div>
                    `;
                }
                
                async function showSection(section) {
                    // Hide all sections
                    document.querySelectorAll('.data-section').forEach(s => s.classList.remove('active'));
                    // Show selected section
                    document.getElementById(section).classList.add('active');
                    
                    // Load data
                    const response = await fetch(`/api/${section}`);
                    const data = await response.json();
                    
                    if (section === 'users') {
                        document.getElementById('users-data').innerHTML = `
                            <table>
                                <tr><th>Name</th><th>ID</th><th>Created</th></tr>
                                ${data.map(user => `
                                    <tr>
                                        <td>${user.name}</td>
                                        <td>${user.id.substring(0, 8)}...</td>
                                        <td>${user.created || 'N/A'}</td>
                                    </tr>
                                `).join('')}
                            </table>
                        `;
                    } else if (section === 'groups') {
                        document.getElementById('groups-data').innerHTML = data.map(group => `
                            <div class="expense-item">
                                <h3>${group.name}</h3>
                                <p><strong>Members:</strong> ${group.members.join(', ')}</p>
                                <p><strong>Created:</strong> ${group.created || 'N/A'}</p>
                            </div>
                        `).join('');
                    } else if (section === 'expenses') {
                        document.getElementById('expenses-data').innerHTML = data.map(expense => `
                            <div class="expense-item">
                                <h3>${expense.name}</h3>
                                <p><strong>Paid by:</strong> ${expense.paid_by}</p>
                                <p><strong>Amount:</strong> $${expense.amount}</p>
                                <p><strong>Split:</strong> ${expense.split_type}</p>
                                <p><strong>Group:</strong> ${expense.group}</p>
                                <p><strong>Date:</strong> ${expense.created || 'N/A'}</p>
                            </div>
                        `).join('');
                    } else if (section === 'settlements') {
                        document.getElementById('settlements-data').innerHTML = data.map(settlement => `
                            <div class="settlement-item">
                                <h3>${settlement.group}</h3>
                                <p><strong>${settlement.borrower}</strong> pays <strong>$${settlement.amount}</strong> to <strong>${settlement.receiver}</strong></p>
                            </div>
                        `).join('');
                    }
                }
                
                // Load stats on page load
                loadStats();
            </script>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_users(self):
        with Database() as db:
            db.cur.execute("SELECT user_id, user_name, created_at FROM users ORDER BY created_at")
            users = [{"id": row[0], "name": row[1], "created": row[2]} for row in db.cur.fetchall()]
        
        self.send_json(users)
    
    def serve_groups(self):
        with Database() as db:
            db.cur.execute("""
                SELECT g.group_id, g.group_name, g.created_at,
                       GROUP_CONCAT(u.user_name) as members
                FROM groups g
                LEFT JOIN group_members gm ON g.group_id = gm.group_id
                LEFT JOIN users u ON gm.user_id = u.user_id
                GROUP BY g.group_id, g.group_name, g.created_at
                ORDER BY g.created_at
            """)
            groups = []
            for row in db.cur.fetchall():
                groups.append({
                    "id": row[0],
                    "name": row[1],
                    "created": row[2],
                    "members": row[3].split(',') if row[3] else []
                })
        
        self.send_json(groups)
    
    def serve_expenses(self):
        with Database() as db:
            db.cur.execute("""
                SELECT e.name, u.user_name as paid_by, e.total_amount, 
                       e.split_type, g.group_name, e.created_at
                FROM expense e
                JOIN users u ON e.paid_by = u.user_id
                JOIN groups g ON e.group_id = g.group_id
                ORDER BY e.created_at DESC
            """)
            expenses = []
            for row in db.cur.fetchall():
                expenses.append({
                    "name": row[0],
                    "paid_by": row[1],
                    "amount": float(row[2]),
                    "split_type": row[3],
                    "group": row[4],
                    "created": row[5]
                })
        
        self.send_json(expenses)
    
    def serve_settlements(self):
        with Database() as db:
            db.cur.execute("""
                SELECT g.group_name, u1.user_name as borrower, u2.user_name as receiver, 
                       bs.amount
                FROM balance_sheet bs
                JOIN groups g ON bs.group_id = g.group_id
                JOIN users u1 ON bs.borrower_id = u1.user_id
                JOIN users u2 ON bs.receiver_id = u2.user_id
                ORDER BY g.group_name, bs.amount DESC
            """)
            settlements = []
            for row in db.cur.fetchall():
                settlements.append({
                    "group": row[0],
                    "borrower": row[1],
                    "receiver": row[2],
                    "amount": float(row[3])
                })
        
        self.send_json(settlements)
    
    def serve_stats(self):
        with Database() as db:
            db.cur.execute("SELECT COUNT(*) FROM users")
            user_count = db.cur.fetchone()[0]
            
            db.cur.execute("SELECT COUNT(*) FROM groups")
            group_count = db.cur.fetchone()[0]
            
            db.cur.execute("SELECT COUNT(*) FROM expense")
            expense_count = db.cur.fetchone()[0]
            
            db.cur.execute("SELECT SUM(total_amount) FROM expense")
            total_amount = db.cur.fetchone()[0] or 0
            
            db.cur.execute("SELECT COUNT(*) FROM balance_sheet")
            settlement_count = db.cur.fetchone()[0]
            
            stats = {
                "users": user_count,
                "groups": group_count,
                "expenses": expense_count,
                "total_amount": float(total_amount),
                "settlements": settlement_count
            }
        
        self.send_json(stats)
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def run_server():
    server = HTTPServer(('localhost', 8000), SplitWiseHandler)
    print("SplitWise Backend Server running at http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.shutdown()

if __name__ == "__main__":
    run_server()