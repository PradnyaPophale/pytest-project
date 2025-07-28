📖 Overview
This project demonstrates a real-world API testing framework built with Pytest for a Flask-based Task Management API.
The framework is designed using best practices followed by 4+ years experienced QA Automation Engineers, covering advanced Pytest concepts such as fixtures, markers, logging, reporting, and reusable test configurations.
The framework supports automated report generation with timestamps and is structured for scalability and maintainability.

🚀 Features
1) Flask-based Task Management App (app.py) – Provides REST API endpoints for basic CRUD operations on tasks.
2_Structured Pytest Framework – Implements fixtures, parameterization, and hooks for efficient testing.
3) Reusable Configurations (pytest.ini, conftest.py) – Centralized configuration and setup/teardown.
🧩 Pytest Concepts Used
✔ Fixtures → For setting up API clients, test data, and teardown
✔ Markers → @pytest.mark.smoke, @pytest.mark.regression, etc.
✔ Logging → Centralized logs with timestamps
✔ Hooks → Used to generate custom reports/logs
✔ Parametrization → Test multiple inputs easily
✔ Configuration → Centralized in pytest.ini

📊 Reports & Logging
HTML test reports generated automatically in /reports/.
Each report file has a timestamp-based filename for history tracking.
Logs are captured for each test execution.

5) Auto HTML report generation
✅ Auto-Generated Reports (reports/) – Test results saved with timestamped filenames.
6) Scalable & Maintainable Design – Easy to extend for more APIs or test cases.

📂 Project Structure

pytest-project/
│── app.py                  # Flask Task Management API logic
│── conftest.py             # Pytest fixtures and hooks
│── pytest.ini              # Pytest configuration (markers, logging)
│── test_flask_app.py       # Test cases for API endpoints
│── requirements.txt        # Required dependencies
│── reports/                # Auto-generated HTML/Allure reports
│── .gitignore              # Ignored files (cache, reports, etc.)

⚙️ Setup & Installation
🔹 1️⃣ Clone the Repository
git clone https://github.com/PradnyaPophale/pytest-project.git
cd pytest-project

🔹 2️⃣ Create Virtual Environment
        python -m venv venv
        source venv/bin/activate   # Mac/Linux
        venv\Scripts\activate      # Windows
🔹 3️⃣ Install Dependencies
        pip install -r requirements.txt
🔹 4️⃣ Run the Flask App
        python app.py
        The API will start at http://127.0.0.1:5000
🧪 Running Tests
✅ Run All Tests
pytest -v
✅ Run Tests with Markers
pytest -v -m smoke
pytest -v -m regression
✅ Generate HTML Report with Timestamp
pytest --html=reports/report_$(date +"%Y%m%d_%H%M%S").html


📌 API Endpoints
Method	Endpoint	Description
GET	/tasks	Fetch all tasks
POST	/tasks	Create a new task
PUT	/tasks/<id>	Update a task by ID
DELETE	/tasks/<id>	Delete a task by ID

🎯 Why This Project is Unique?
✅ Shows real-world framework skills expected from a 4+ year experienced QA Automation Engineer.
✅ Demonstrates API testing from scratch (Flask app + Pytest framework).
✅ Implements scalable, maintainable, and CI/CD-ready testing structure.

🔮 Future Enhancements
🔹 Integrate with GitHub Actions / Jenkins for CI/CD
🔹 Store reports in S3 or artifacts
🔹 Add Allure reports for rich test visualization
🔹 Extend API with authentication & DB integration

📌 Author
👩‍💻 Pradnya Pophale
📧 [pophalepradnya524@gmail.com]
🌐 [https://www.linkedin.com/in/pradnya-pophale-756ab1184/]

