from flask import Flask, jsonify, request, render_template_string
from datetime import datetime, timedelta
import uuid
from functools import wraps
import hashlib

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# In-memory databases
users = {
    1: {
        "id": 1, 
        "name": "Pradnya", 
        "email": "pradnya@example.com",
        "password": hashlib.sha256("password123".encode()).hexdigest(),
        "created_at": datetime.now().isoformat(),
        "is_active": True
    },
    2: {
        "id": 2, 
        "name": "John", 
        "email": "john@example.com",
        "password": hashlib.sha256("password123".encode()).hexdigest(),
        "created_at": datetime.now().isoformat(),
        "is_active": True
    },
    3: {
        "id": 3, 
        "name": "Jacky", 
        "email": "jackyy@example.com",
        "password": hashlib.sha256("password123".encode()).hexdigest(),
        "created_at": datetime.now().isoformat(),
        "is_active": True
    },
}

projects = {
    1: {
        "id": 1,
        "name": "Personal Development",
        "description": "Self-improvement tasks",
        "owner_id": 1,
        "created_at": datetime.now().isoformat(),
        "status": "active"
    },
    2: {
        "id": 2,
        "name": "Work Projects",
        "description": "Professional tasks",
        "owner_id": 1,
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }
}

tasks = {
    1: {
        "id": 1,
        "title": "Learn Flask Advanced Features",
        "description": "Study Flask blueprints, authentication, and database integration",
        "project_id": 1,
        "assigned_to": 1,
        "created_by": 1,
        "priority": "high",
        "status": "in_progress",
        "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "tags": ["learning", "programming"]
    },
    2: {
        "id": 2,
        "title": "Complete API Documentation",
        "description": "Document all endpoints with examples",
        "project_id": 2,
        "assigned_to": 2,
        "created_by": 1,
        "priority": "medium",
        "status": "todo",
        "due_date": (datetime.now() + timedelta(days=3)).isoformat(),
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "tags": ["documentation", "work"]
    }
}

sessions = {}

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token not in sessions:
            return jsonify({"error": "Authentication required"}), 401
        
        user_id = sessions[token]
        if user_id not in users:
            return jsonify({"error": "Invalid session"}), 401
        
        request.current_user = users[user_id]
        return f(*args, **kwargs)
    return decorated_function

# HTML Template for the dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #e9ecef;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background-color: #B6DA9F;
            color: #06402B;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin: 0;
        }
        
        .header p {
            font-size: 1.2em;
        }
        
        .stats {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            flex: 1;
            transition: transform 0.2s;
        }
        
        .stat-card:hover {
            transform: scale(1.05);
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }
        
        .projects, .tasks {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        
        .project-item, .task-item {
            padding: 15px;
            border-left: 4px solid #007bff;
            margin-bottom: 10px;
            background: #f8f9fa;
            transition: background 0.3s;
        }
        
        .project-item:hover, .task-item:hover {
            background: #f1f1f1;
        }
        
        .priority-high { border-left-color: #e74c3c; }
        .priority-medium { border-left-color: #f39c12; }
        .priority-low { border-left-color: #27ae60; }
        
        .status-completed { background-color: #d5f4e6; }
        .status-in-progress { background-color: #fff3cd; }
        
        .api-info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        .endpoint {
            background: #343a40;
            color: white;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            font-family: monospace;
            transition: background 0.3s;
        }
        
        .endpoint:hover {
            background: #495057;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .stats {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Task Management Dashboard</h1>
            <p>Welcome to your personal task management system</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ stats.total_tasks }}</div>
                <div>Total Tasks</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.completed_tasks }}</div>
                <div>Completed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.pending_tasks }}</div>
                <div>Pending</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.total_projects }}</div>
                <div>Projects</div>
            </div>
        </div>
        
        <div class="projects">
            <h2>🚀 Active Projects</h2>
            {% for project in projects %}
            <div class="project-item">
                <strong>{{ project.name }}</strong>
                <p>{{ project.description }}</p>
                <small>Tasks: {{ project.task_count }} | Created: {{ project.created_at[:10] }}</small>
            </div>
            {% endfor %}
        </div>
        
        <div class="tasks">
            <h2>📝 Recent Tasks</h2>
            {% for task in tasks %}
            <div class="task-item priority-{{ task.priority }} status-{{ task.status }}">
                <strong>{{ task.title }}</strong>
                <p>{{ task.description }}</p>
                <div>
                    <span style="background: #3498db; color: white; padding: 2px 6px; border-radius: 3px; font-size: 12px;">{{ task.priority.upper() }}</span>
                    <span style="background: #27ae60; color: white; padding: 2px 6px; border-radius: 3px; font-size: 12px; margin-left: 5px;">{{ task.status.upper() }}</span>
                    {% if task.due_date %}
                    <span style="color: #7f8c8d; font-size: 12px; margin-left: 10px;">Due: {{ task.due_date[:10] }}</span>
                    {% endif %}
                </div>
                <div style="margin-top: 5px;">
                    {% for tag in task.tags %}
                    <span style="background: #ecf0f1; padding: 2px 6px; border-radius: 3px; font-size: 11px; margin-right: 5px;">#{{ tag }}</span>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>
        
    <div class="api-info" style="background-color: #f4f7f6; border: 1px solid #e0e0e0; border-radius: 8px; padding: 25px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); max-width: 600px; margin: 30px auto; color: #333;">
        <h2 style="color: #2c3e50; text-align: center; margin-bottom: 20px; font-size: 1.8em; border-bottom: 2px solid #5fa2dd; padding-bottom: 10px;">🔌 API Endpoints</h2>
        <p style="text-align: center; margin-bottom: 25px; color: #555; font-size: 1.1em;">Use these endpoints to interact with the task management system:</p>
        <div class="endpoint" style="background-color: #ffffff; border: 1px solid #dcdcdc; border-left: 5px solid #27ae60; border-radius: 6px; padding: 15px 20px; margin-bottom: 15px; color: #333; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);">
            <strong style="color: #27ae60;">POST</strong> /auth/login - Login with email and password
        </div>
        <div class="endpoint" style="background-color: #f9f9f9; border: 1px solid #dcdcdc; border-left: 5px solid #2980b9; border-radius: 6px; padding: 15px 20px; margin-bottom: 15px; color: #333; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);">
            <strong style="color: #2980b9;">GET</strong> /users/profile - Get current user profile
        </div>
        <div class="endpoint" style="background-color: #ffffff; border: 1px solid #dcdcdc; border-left: 5px solid #2980b9; border-radius: 6px; padding: 15px 20px; margin-bottom: 15px; color: #333; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);">
            <strong style="color: #2980b9;">GET</strong> /projects - Get all projects
        </div>
        <div class="endpoint" style="background-color: #f9f9f9; border: 1px solid #dcdcdc; border-left: 5px solid #27ae60; border-radius: 6px; padding: 15px 20px; margin-bottom: 15px; color: #333; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);">
            <strong style="color: #27ae60;">POST</strong> /projects - Create new project
        </div>
        <div class="endpoint" style="background-color: #ffffff; border: 1px solid #dcdcdc; border-left: 5px solid #2980b9; border-radius: 6px; padding: 15px 20px; margin-bottom: 15px; color: #333; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);">
            <strong style="color: #2980b9;">GET</strong> /tasks - Get tasks (with filters)
        </div>
        <div class="endpoint" style="background-color: #f9f9f9; border: 1px solid #dcdcdc; border-left: 5px solid #27ae60; border-radius: 6px; padding: 15px 20px; margin-bottom: 15px; color: #333; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);">
            <strong style="color: #27ae60;">POST</strong> /tasks - Create new task
        </div>
        <div class="endpoint" style="background-color: #ffffff; border: 1px solid #dcdcdc; border-left: 5px solid #2980b9; border-radius: 6px; padding: 15px 20px; margin-bottom: 15px; color: #333; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);">
            <strong style="color: #2980b9;">GET</strong> /analytics/dashboard - Get dashboard analytics
        </div>
    </div>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    # Calculate stats
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks.values() if t['status'] == 'completed'])
    pending_tasks = total_tasks - completed_tasks
    total_projects = len(projects)
    
    # Get project data with task counts
    project_data = []
    for project in projects.values():
        project_tasks = [t for t in tasks.values() if t['project_id'] == project['id']]
        project_data.append({
            **project,
            'task_count': len(project_tasks)
        })
    
    # Get recent tasks
    recent_tasks = list(tasks.values())[:5]
    
    return render_template_string(DASHBOARD_TEMPLATE, 
                                stats={
                                    'total_tasks': total_tasks,
                                    'completed_tasks': completed_tasks,
                                    'pending_tasks': pending_tasks,
                                    'total_projects': total_projects
                                },
                                projects=project_data,
                                tasks=recent_tasks)

# Authentication endpoints
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    # Find user by email
    user = None
    for u in users.values():
        if u['email'] == email:
            user = u
            break
    
    if not user or user['password'] != hashlib.sha256(password.encode()).hexdigest():
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Create session
    token = str(uuid.uuid4())
    sessions[token] = user['id']
    
    return jsonify({
        "token": token,
        "user": {
            "id": user['id'],
            "name": user['name'],
            "email": user['email']
        }
    }), 200

@app.route("/auth/logout", methods=["POST"])
@require_auth
def logout():
    token = request.headers.get('Authorization')
    if token in sessions:
        del sessions[token]
    return jsonify({"message": "Logged out successfully"}), 200

# Enhanced User endpoints
@app.route("/users/profile", methods=["GET"])
@require_auth
def get_profile():
    user = request.current_user
    user_tasks = [t for t in tasks.values() if t['assigned_to'] == user['id']]
    user_projects = [p for p in projects.values() if p['owner_id'] == user['id']]
    
    return jsonify({
        "user": {
            "id": user['id'],
            "name": user['name'],
            "email": user['email'],
            "created_at": user['created_at']
        },
        "stats": {
            "total_tasks": len(user_tasks),
            "completed_tasks": len([t for t in user_tasks if t['status'] == 'completed']),
            "projects": len(user_projects)
        }
    }), 200

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({
            "id": user['id'],
            "name": user['name'],
            "email": user['email'],
            "created_at": user['created_at'],
            "is_active": user['is_active']
        }), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    
    # Validation
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Name, email, and password are required"}), 400
    
    # Check if email already exists
    for user in users.values():
        if user['email'] == data['email']:
            return jsonify({"error": "Email already exists"}), 400
    
    new_id = max(users.keys()) + 1 if users else 1
    users[new_id] = {
        "id": new_id,
        "name": data['name'],
        "email": data['email'],
        "password": hashlib.sha256(data['password'].encode()).hexdigest(),
        "created_at": datetime.now().isoformat(),
        "is_active": True
    }
    
    return jsonify({
        "id": new_id,
        "name": data['name'],
        "email": data['email'],
        "created_at": users[new_id]['created_at']
    }), 201

# Project endpoints
@app.route("/projects", methods=["GET"])
@require_auth
def get_projects():
    user_id = request.current_user['id']
    user_projects = [p for p in projects.values() if p['owner_id'] == user_id]
    
    # Add task counts to projects
    for project in user_projects:
        project['task_count'] = len([t for t in tasks.values() if t['project_id'] == project['id']])
    
    return jsonify(user_projects), 200

@app.route("/projects", methods=["POST"])
@require_auth
def create_project():
    data = request.json
    user_id = request.current_user['id']
    
    if not data.get('name'):
        return jsonify({"error": "Project name is required"}), 400
    
    new_id = max(projects.keys()) + 1 if projects else 1
    projects[new_id] = {
        "id": new_id,
        "name": data['name'],
        "description": data.get('description', ''),
        "owner_id": user_id,
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    return jsonify(projects[new_id]), 201

@app.route("/projects/<int:project_id>", methods=["PUT"])
@require_auth
def update_project(project_id):
    user_id = request.current_user['id']
    project = projects.get(project_id)
    
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    if project['owner_id'] != user_id:
        return jsonify({"error": "Not authorized"}), 403
    
    data = request.json
    project.update({
        "name": data.get('name', project['name']),
        "description": data.get('description', project['description']),
        "status": data.get('status', project['status'])
    })
    
    return jsonify(project), 200

# Task endpoints
@app.route("/tasks", methods=["GET"])
@require_auth
def get_tasks():
    user_id = request.current_user['id']
    
    # Filter parameters
    project_id = request.args.get('project_id', type=int)
    status = request.args.get('status')
    priority = request.args.get('priority')
    
    # Get tasks assigned to user
    user_tasks = [t for t in tasks.values() if t['assigned_to'] == user_id]
    
    # Apply filters
    if project_id:
        user_tasks = [t for t in user_tasks if t['project_id'] == project_id]
    if status:
        user_tasks = [t for t in user_tasks if t['status'] == status]
    if priority:
        user_tasks = [t for t in user_tasks if t['priority'] == priority]
    
    return jsonify(user_tasks), 200

@app.route("/tasks", methods=["POST"])
@require_auth
def create_task():
    data = request.json
    user_id = request.current_user['id']
    
    if not data.get('title'):
        return jsonify({"error": "Task title is required"}), 400
    
    project_id = data.get('project_id')
    if project_id and project_id not in projects:
        return jsonify({"error": "Invalid project"}), 400
    
    new_id = max(tasks.keys()) + 1 if tasks else 1
    tasks[new_id] = {
        "id": new_id,
        "title": data['title'],
        "description": data.get('description', ''),
        "project_id": project_id,
        "assigned_to": data.get('assigned_to', user_id),
        "created_by": user_id,
        "priority": data.get('priority', 'medium'),
        "status": data.get('status', 'todo'),
        "due_date": data.get('due_date'),
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "tags": data.get('tags', [])
    }
    
    return jsonify(tasks[new_id]), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
@require_auth
def update_task(task_id):
    user_id = request.current_user['id']
    task = tasks.get(task_id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    if task['assigned_to'] != user_id and task['created_by'] != user_id:
        return jsonify({"error": "Not authorized"}), 403
    
    data = request.json
    
    # If marking as completed, set completion time
    if data.get('status') == 'completed' and task['status'] != 'completed':
        data['completed_at'] = datetime.now().isoformat()
    
    task.update(data)
    return jsonify(task), 200

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@require_auth
def delete_task(task_id):
    user_id = request.current_user['id']
    task = tasks.get(task_id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    if task['created_by'] != user_id:
        return jsonify({"error": "Not authorized"}), 403
    
    deleted_task = tasks.pop(task_id)
    return jsonify(deleted_task), 200

# Analytics endpoints
@app.route("/analytics/dashboard", methods=["GET"])
@require_auth
def get_dashboard_analytics():
    user_id = request.current_user['id']
    user_tasks = [t for t in tasks.values() if t['assigned_to'] == user_id]
    user_projects = [p for p in projects.values() if p['owner_id'] == user_id]
    
    # Task status distribution
    status_counts = {}
    for task in user_tasks:
        status = task['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Priority distribution
    priority_counts = {}
    for task in user_tasks:
        priority = task['priority']
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    # Overdue tasks
    overdue_tasks = []
    for task in user_tasks:
        if task['due_date'] and task['status'] != 'completed':
            due_date = datetime.fromisoformat(task['due_date'])
            if due_date < datetime.now():
                overdue_tasks.append(task)
    
    return jsonify({
        "total_tasks": len(user_tasks),
        "total_projects": len(user_projects),
        "status_distribution": status_counts,
        "priority_distribution": priority_counts,
        "overdue_tasks": len(overdue_tasks),
        "completion_rate": len([t for t in user_tasks if t['status'] == 'completed']) / len(user_tasks) * 100 if user_tasks else 0
    }), 200

# Legacy user endpoints (for backward compatibility)
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    # Don't allow password updates through this endpoint
    if 'password' in data:
        del data['password']
    
    users[user_id].update(data)
    return jsonify({
        "id": users[user_id]['id'],
        "name": users[user_id]['name'],
        "email": users[user_id]['email'],
        "created_at": users[user_id]['created_at']
    }), 200

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id in users:
        deleted = users.pop(user_id)
        return jsonify({
            "id": deleted['id'],
            "name": deleted['name'],
            "email": deleted['email']
        }), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    print("🚀Task Management System Starting...")
    print("📋 Dashboard: http://127.0.0.1:5000")
    print("🔐 Login credentials:")
    print("   Email: pradnya@example.com, Password: password123")
    print("   Email: john@example.com, Password: password123")
    print("🔌 API Documentation available at the dashboard")
    app.run(debug=True, host="127.0.0.1", port=5000)