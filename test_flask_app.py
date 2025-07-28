import pytest
import subprocess
import time
import os
import signal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE = "http://127.0.0.1:5000"

@pytest.fixture(scope="session", autouse=True)
def start_flask_app():
    # Start Flask app in background
    process = subprocess.Popen(["python", "app.py"])
    time.sleep(2)  # wait for server to start

    yield  # run the tests

    # Teardown: Kill the Flask server
    if os.name == "nt":
        process.terminate()
    else:
        os.kill(process.pid, signal.SIGTERM)
    process.wait()

class TestAuthenticationEndpoints:
    """Test authentication related endpoints."""

    @pytest.mark.auth
    def test_login_success(self, client):
        """Test successful login with valid credentials."""
        response = client.post('/auth/login', json={
            'email': 'pradnya@example.com',
            'password': 'password123'
        })

        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
        assert 'user' in data
        assert data['user']['email'] == 'pradnya@example.com'
        assert data['user']['name'] == 'Pradnya'

    @pytest.mark.auth
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post('/auth/login', json={
            'email': 'pradnya@example.com',
            'password': 'wrongpassword'
        })

        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'Invalid credentials'

    @pytest.mark.auth
    def test_logout_success(self, client, auth_headers):
        """Test successful logout."""
        response = client.post('/auth/logout', headers=auth_headers)

        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Logged out successfully'


class TestUserEndpoints:
    """Test user-related CRUD operations."""

    @pytest.mark.crud
    def test_create_user_success(self, client, sample_user_data):
        """Test successful user creation (POST)."""
        response = client.post('/users', json=sample_user_data)

        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == sample_user_data['name']
        assert data['email'] == sample_user_data['email']
        assert 'id' in data
        assert 'created_at' in data

    @pytest.mark.crud
    def test_get_user_success(self, client):
        """Test getting user by ID (GET)."""
        response = client.get('/users/1')

        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == 1
        assert data['name'] == 'Pradnya'
        assert data['email'] == 'pradnya@example.com'

    @pytest.mark.crud
    def test_update_user_success(self, client):
        """Test updating user (PUT)."""
        update_data = {
            'name': 'Updated Pradnya',
            'email': 'updated.pradnya@example.com'
        }

        response = client.put('/users/1', json=update_data)

        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'Updated Pradnya'
        assert data['email'] == 'updated.pradnya@example.com'

    @pytest.mark.crud
    def test_delete_user_success(self, client):
        """Test deleting user (DELETE)."""
        response = client.delete('/users/1')

        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == 1
        assert data['name'] == 'Pradnya'

        # Verify user is deleted
        response = client.get('/users/1')
        assert response.status_code == 404


class TestProjectEndpoints:
    """Test project-related CRUD operations."""

    @pytest.mark.crud
    def test_create_project_success(self, client, auth_headers, sample_project_data):
        """Test successful project creation (POST)."""
        response = client.post('/projects', json=sample_project_data, headers=auth_headers)

        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == sample_project_data['name']
        assert data['description'] == sample_project_data['description']
        assert data['owner_id'] == 1
        assert data['status'] == 'active'

    @pytest.mark.crud
    def test_get_projects_success(self, client, auth_headers):
        """Test getting all projects for authenticated user (GET)."""
        response = client.get('/projects', headers=auth_headers)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2  # Initial data has 2 projects for user 1
        assert all('task_count' in project for project in data)

    @pytest.mark.crud
    def test_update_project_success(self, client, auth_headers):
        """Test updating project (PUT)."""
        update_data = {
            'name': 'Updated Project Name',
            'description': 'Updated description',
            'status': 'inactive'
        }

        response = client.put('/projects/1', json=update_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'Updated Project Name'
        assert data['description'] == 'Updated description'
        assert data['status'] == 'inactive'


class TestTaskEndpoints:
    """Test task-related CRUD operations."""

    @pytest.mark.crud
    def test_create_task_success(self, client, auth_headers, sample_task_data):
        """Test successful task creation (POST)."""
        response = client.post('/tasks', json=sample_task_data, headers=auth_headers)

        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == sample_task_data['title']
        assert data['description'] == sample_task_data['description']
        assert data['priority'] == sample_task_data['priority']
        assert data['status'] == sample_task_data['status']
        assert data['assigned_to'] == 1
        assert data['created_by'] == 1

    @pytest.mark.crud
    def test_get_tasks_with_filters(self, client, auth_headers):
        """Test getting tasks with filters (GET)."""
        # Test getting all tasks
        response = client.get('/tasks', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1  # User 1 has 1 task assigned

        # Test filtering by status
        response = client.get('/tasks?status=in_progress', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert all(task['status'] == 'in_progress' for task in data)

        # Test filtering by priority
        response = client.get('/tasks?priority=high', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert all(task['priority'] == 'high' for task in data)

    @pytest.mark.crud
    def test_update_task_success(self, client, auth_headers):
        """Test updating task (PUT)."""
        update_data = {
            'title': 'Updated Task Title',
            'status': 'completed',
            'priority': 'low'
        }

        response = client.put('/tasks/1', json=update_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Updated Task Title'
        assert data['status'] == 'completed'
        assert data['priority'] == 'low'
        assert data['completed_at'] is not None

    @pytest.mark.crud
    def test_delete_task_success(self, client, auth_headers):
        """Test deleting task (DELETE)."""
        response = client.delete('/tasks/1', headers=auth_headers)

        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == 1
        assert data['title'] == 'Learn Flask Advanced Features'

        # Verify task is deleted
        response = client.get('/tasks', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 0


class TestAnalyticsEndpoints:
    """Test analytics and dashboard endpoints."""

    @pytest.mark.api
    def test_dashboard_analytics(self, client, auth_headers):
        """Test dashboard analytics endpoint (GET)."""
        response = client.get('/analytics/dashboard', headers=auth_headers)

        assert response.status_code == 200
        data = response.get_json()
        assert 'total_tasks' in data
        assert 'total_projects' in data
        assert 'status_distribution' in data
        assert 'priority_distribution' in data
        assert 'overdue_tasks' in data
        assert 'completion_rate' in data
        assert isinstance(data['completion_rate'], (int, float))

    @pytest.mark.api
    def test_user_profile(self, client, auth_headers):
        """Test user profile endpoint (GET)."""
        response = client.get('/users/profile', headers=auth_headers)

        assert response.status_code == 200
        data = response.get_json()
        assert 'user' in data
        assert 'stats' in data
        assert data['user']['id'] == 1
        assert data['user']['name'] == 'Pradnya'
        assert 'total_tasks' in data['stats']
        assert 'completed_tasks' in data['stats']
        assert 'projects' in data['stats']


class TestAuthorizationAndSecurity:
    """Test authorization and security aspects."""

    @pytest.mark.auth
    def test_protected_route_without_auth(self, client):
        """Test accessing protected route without authentication."""
        response = client.get('/users/profile')

        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'Authentication required'

    @pytest.mark.auth
    def test_update_other_users_task_forbidden(self, client, logged_in_user_2):
        """Test that users cannot update tasks they don't own."""
        update_data = {'title': 'Trying to update'}

        # User 2 trying to update task 1 (owned by user 1)
        response = client.put('/tasks/1', json=update_data, headers=logged_in_user_2)

        assert response.status_code == 403
        data = response.get_json()
        assert data['error'] == 'Not authorized'

    @pytest.mark.auth
    def test_update_other_users_project_forbidden(self, client, logged_in_user_2):
        """Test that users cannot update projects they don't own."""
        update_data = {'name': 'Trying to update'}

        # User 2 trying to update project 1 (owned by user 1)
        response = client.put('/projects/1', json=update_data, headers=logged_in_user_2)

        assert response.status_code == 403
        data = response.get_json()
        assert data['error'] == 'Not authorized'


class TestErrorHandling:
    """Test error handling and edge cases."""

    @pytest.mark.api
    def test_create_user_missing_fields(self, client):
        """Test creating user with missing required fields."""
        response = client.post('/users', json={
            'name': 'Test User'
            # Missing email and password
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    @pytest.mark.api
    def test_create_user_duplicate_email(self, client):
        """Test creating user with duplicate email."""
        response = client.post('/users', json={
            'name': 'Test User',
            'email': 'pradnya@example.com',  # Already exists
            'password': 'password123'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Email already exists'

    @pytest.mark.api
    def test_get_nonexistent_user(self, client):
        """Test getting non-existent user."""
        response = client.get('/users/999')

        assert response.status_code == 404
        data = response.get_json()
        logger.info(data)
        assert data['error'] == 'User not found'

    @pytest.mark.api
    def test_create_task_invalid_project(self, client, auth_headers):
        """Test creating task with invalid project ID."""
        task_data = {
            'title': 'Test Task',
            'project_id': 999  # Non-existent project
        }

        response = client.post('/tasks', json=task_data, headers=auth_headers)

        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Invalid project'


class TestHomeDashboard:
    """Test the home dashboard endpoint."""

    @pytest.mark.api
    def test_home_dashboard_renders(self, client):
        """Test that the home dashboard renders successfully."""
        response = client.get('/')
        logger.info("Home Dashboard Response: %s", response.data)
        assert response.status_code == 200
        assert b'Task Management Dashboard' in response.data
        assert b'Total Tasks' in response.data
        assert b'Active Projects' in response.data
        assert b'Recent Tasks' in response.data
        assert b'API Endpoints' in response.data