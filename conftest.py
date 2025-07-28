import pytest
import sys
import os
from datetime import datetime, timedelta
import hashlib

# Add the parent directory to the path so we can import our Flask app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, users, projects, tasks, sessions

def pytest_configure(config):
    report_dir = "report"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(report_dir, f"report_{timestamp}.html")

    config.option.htmlpath = report_path  # override --html argument


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'

    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def auth_headers(client):
    """Create authentication headers for testing protected routes."""
    # Login with test user
    response = client.post('/auth/login', json={
        'email': 'pradnya@example.com',
        'password': 'password123'
    })

    assert response.status_code == 200
    token = response.get_json()['token']

    return {'Authorization': token}


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        'name': 'Test User',
        'email': 'testuser@example.com',
        'password': 'testpass123'
    }


@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        'name': 'Test Project',
        'description': 'A test project for pytest'
    }


@pytest.fixture
def sample_task_data():
    """Sample task data for testing."""
    return {
        'title': 'Test Task',
        'description': 'A test task for pytest',
        'project_id': 1,
        'priority': 'high',
        'status': 'todo',
        'due_date': (datetime.now() + timedelta(days=5)).isoformat(),
        'tags': ['test', 'pytest']
    }


@pytest.fixture(autouse=True)
def reset_data():
    """Reset the in-memory data before each test."""
    # Clear all data
    users.clear()
    projects.clear()
    tasks.clear()
    sessions.clear()

    # Restore initial data
    users.update({
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
    })

    projects.update({
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
    })

    tasks.update({
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
    })

    yield

    # Clean up after test
    users.clear()
    projects.clear()
    tasks.clear()
    sessions.clear()


@pytest.fixture
def logged_in_user_2(client):
    """Create authentication headers for user 2."""
    response = client.post('/auth/login', json={
        'email': 'john@example.com',
        'password': 'password123'
    })

    assert response.status_code == 200
    token = response.get_json()['token']

    return {'Authorization': token}

# Example fixture to log each test using this
@pytest.fixture(autouse=True)
def log_test_name(request):
    print(f"\n Running test: {request.node.name}")